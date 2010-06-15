import os, struct, collections, copy, logging, Queue
from freequery.index.inverted_index_pb2 import InvertedIndexEntry as proto_InvertedIndexEntry, Posting as proto_Posting
from freequery.lang.terms import prep_term


size_header = struct.Struct('I')
SYNC = "\x99\x00\x00\x00\x00\x00\x00\x98"

class InvertedIndex(object):

    def __init__(self, path):
        """
        Opens an inverted index at `path`.
        """
        self.path = path
    
    def __unicode__(self):
        return "<%s path='%s'>" % (self.__class__.__name__, self.path)

    __str__ = __unicode__
    __repr__ = __unicode__

    
class InvertedIndexReader(InvertedIndex):

    """
    Reads and queries an inverted index.
    """

    def __init__(self, path):
        super(InvertedIndexReader, self).__init__(path)
        self.__open_file()

    def __open_file(self):
        self.file = open(self.path, 'rb')

    def close(self):
        """Closes the index file."""
        self.file.close()
        self.file = None
        
    def __iter__(self):
        return InvertedIndexIterator(self.path)
        
    def lookup(self, token):
        """Returns a list of postings for `Document`s that contain `token`."""
        term = prep_term(token)

        # find the entry using binary search
        n = os.path.getsize(self.path)
        lo = 0
        hi = n
        while lo < hi:
            mid = (lo+hi)/2
            e = self.__entry_containing_offset(mid)
            if e.term < term:
                lo = mid + 1
            else:
                hi = mid
        e_lo = self.__entry_containing_offset(lo)
        if lo < n and e_lo.term == term:
            return e_lo.postings
        else:
            return []
        
    def __entry_containing_offset(self, ofs):
        """Returns the first entry that begins before or at `ofs`."""
        # find the start of the first sync before `ofs`
        synclen = len(SYNC)
        pos = ofs - synclen
        while True:
            if pos <= 0:
                return self.__entry_at(0)
            self.file.seek(pos)
            if self.file.read(synclen) == SYNC:
                return self.__entry_at(pos + synclen)
            pos -= 1

    def __entry_at(self, ofs):
        self.file.seek(ofs, os.SEEK_SET)
        sizedata = self.file.read(size_header.size)
        if len(sizedata) != size_header.size:
            raise Exception("expected size header but got EOF at ofs=%d" % ofs)
        size = size_header.unpack(sizedata)[0]
        data = self.file.read(size)
        e = proto_InvertedIndexEntry()
        e.ParseFromString(data)
        return e
    

class InvertedIndexIterator(object):

    def __init__(self, path):
        self.file = open(path, 'rb')

    def next(self):
        try:
            data = self.file.read(size_header.size)
            if len(data) != size_header.size:
                raise EOFError
            size = size_header.unpack(data)[0]
        except EOFError:
            self.file.close()
            raise StopIteration
        data = self.file.read(size)
        self.file.seek(len(SYNC), os.SEEK_CUR) # sync past SYNC
        e = proto_InvertedIndexEntry()
        e.ParseFromString(data)
        return e

    def __iter__(self):
        return self


class InvertedIndexWriter(InvertedIndex):

    """
    Writes an inverted index.
    """

    def __init__(self, path, postings_per_tmp_file=20000):
        self.path = path
        self.postings_per_tmp_file = postings_per_tmp_file
        self.tmp_num = 0
        self.tmp_files = []
        self.tmp_file = None
        self.__open_file()
        self.__open_new_tmp_file()

    def __open_file(self):
        self.file = open(self.path, 'w+b')
        
    def __tmp_file_path(self, n):
        return self.path + '%03d' % n
        
    def __open_new_tmp_file(self):
        tmp_path = self.__tmp_file_path(self.tmp_num)
        if os.path.exists(tmp_path):
            raise Exception("tmp file already exists at %s" % tmp_path)
        self.tmp_file = open(tmp_path, 'w+b')

        self.tmp_files.append(self.tmp_num)
        self.postings = collections.defaultdict(list)
        self.tmp_file_postings = 0
        self.saved = False

    def __close_tmp_file(self):
        self.tmp_file.flush()
        self.tmp_file.close()
        self.tmp_file = None
        self.tmp_file_postings = 0
        self.tmp_num += 1

    def clear(self):
        """Removes the index file. TODO: Should also remove tmp files."""
        if self.tmp_file:
            self.__close_tmp_file()
        for i in self.tmp_files:
            os.remove(self.__tmp_file_path(i))
        
        self.file.close()
        os.remove(self.path)
        
    def add(self, e):
        """Adds a `ForwardIndexEntry` `e` to the inverted index in memory."""
        if self.saved:
            raise NotImplementedError("can't add to index after saving")
        docid = e.docid
        term_hits = e.term_hits
        for th in term_hits:
            posting = proto_Posting()
            posting.docid = docid
            for th_hit in th.hits:
                h = posting.hits.add()
                h.CopyFrom(th_hit)
            self.postings[th.term].append(posting)
            self.tmp_file_postings += 1

        if self.tmp_file_postings >= self.postings_per_tmp_file:
            logging.debug("tmpfile %d full; writing to disk." \
                          % self.tmp_num)
            self.write_to_tmp_file()
            self.__close_tmp_file()
            self.__open_new_tmp_file()
            
    def write_to_tmp_file(self):
        terms = self.postings.keys()
        terms.sort()

        entry = proto_InvertedIndexEntry()

        for term in terms:
            entry.term = term
            for posting in self.postings[term]:
                proto_posting = entry.postings.add()
                proto_posting.CopyFrom(posting)
            s = entry.SerializeToString()
            size = entry.ByteSize()
            self.tmp_file.write(size_header.pack(size))
            self.tmp_file.write(s)
            self.tmp_file.write(SYNC)
            entry.Clear()

    def finish(self):
        if self.tmp_file:
            self.write_to_tmp_file()
            self.__close_tmp_file()

        if len(self.tmp_files) == 0:
            return

        logging.debug("merging tmp_files=%r" % self.tmp_files)
        tmp_file_readers = [InvertedIndexReader(self.__tmp_file_path(i)) \
                            for i in self.tmp_files]
        m = Merger(self.file, tmp_file_readers)
        m.merge()

        self.file.flush()
        self.file.close()

class Merger(object):

    def __init__(self, mainfile, tmp_file_readers):
        self.file = mainfile
        self.readers = [r.__iter__() for r in tmp_file_readers]
        self.term_pqueue = Queue.PriorityQueue()

    def merge(self):
        """
        Merge: step through the postings in each tmp file,
        which are sorted by term, merging them into the main file.
        """
        # fill pqueue initially
        for reader in self.readers:
            self.__enqueue_next_term_in_reader(reader)
            
        cur_term = None
        entry_buf = []
        while not self.term_pqueue.empty():
            item = self.term_pqueue.get_nowait()
            this_term = item[0]
            this_reader = item[1][0]
            this_entry = item[1][1]

            if this_term != cur_term:
                # finished writing this term's postings - no other tmp file
                # has postings for this term or else it would have been
                # returned by term_pqueue
                self.__write_term(entry_buf)
                
                entry_buf = []
                cur_term = this_term

            # concatenating protobuf messages with repeated fields just extends
            # the list of repeated items
            entry_buf.append(this_entry.SerializeToString())

            # get the next term from the reader we took this_term from
            self.__enqueue_next_term_in_reader(this_reader)
            
        # finish writing last term
        self.__write_term(entry_buf)
        entry_buf = []

    def __enqueue_next_term_in_reader(self, reader):
        try:
            reader_next_entry = reader.next()
            if reader_next_entry:
                item = (reader_next_entry.term, (reader, reader_next_entry))
                self.term_pqueue.put_nowait(item)
        except StopIteration:
            pass    
        
    def __write_term(self, entry_buf):
        s = ''.join(entry_buf)
        size = len(s)
        self.file.write(size_header.pack(size))
        self.file.write(s)
        self.file.write(SYNC)
