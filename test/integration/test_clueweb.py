from freequery.test import IntegrationTestCase

class TestClueWebChinese(IntegrationTestCase):
    dumps = ['ClueWeb09_Chinese_Sample']
    expected_results = {
        'richiezhangzhi': [
            'http://www.139mlife.com/bbs/forum-129-1.html',
            'http://www.139mlife.com/bbs/digest.php',
            ]
    }
    index = True
    rank = True

class TestClueWebEnglish(IntegrationTestCase):
    dumps = ['ClueWeb09_English_Sample']
    expected_results = {
        'hello': ['http://www.snowdirt.com/index.html'],
        'university': [
            'http://www.snaption.net/med/index3.htm',
            'http://www.snlonline.net/Prospects/program_info.asp',
            'http://www.snowyrangegraphics.com/Links.html',
            'http://www.smdep.org/transexceptions.htm',
            'http://www.snips.8m.com/home.htm',
            'http://www.snlonline.net/Prospects/Prospect_faq.asp',
            'http://www.smdep.org/progsites/yale',
            ],
        'california': [
            'http://www.smithsbakeries.com/index.htm',
            'http://www.smithsbakeries.com/location/index.htm',
            'http://www.sncs.org/grass-valley-family.htm',
            'http://www.smooth-transition.com/index.html',
            ]
    }
    index = True
    rank = True

    # TODO(sqs): Because two URLs with the same score sort arbitrarily, this is
    # sometimes different (about 1/6 of the time). Should make a more stable
    # way of checking expected ranking that doesn't care if same-ranked pages
    # are out of order.
    expected_ranking = ['http://www.smite.co.id/', 'http://www.smhsknights.org/fieldhockey.htm', 'http://www.smc-it.org/comingsoon.html', 'http://www.snowwhite.ch/e/mobile_tunes.htm', 'http://www.smokefreecoalition.org/about/', 'http://www.snaption.net/med/index3.htm', 'http://www.smd.net.au/contact/', 'http://www.smd.net.au/', 'http://www.smithwalls.com/index.html', 'http://www.smithwalls.com/page/company.html', 'http://www.snowballventures.com/installations.html', 'http://www.snowballventures.com/aboutus.html', 'http://www.smcs.on.ca/giving.htm', 'http://www.smokefreecoalition.org/issues/', 'http://www.snookergods.com/top-snooker-players/', 'http://www.snookergods.com/snooker-betting-options/', 'http://www.smithsbakeries.com/index.htm', 'http://www.smithsbakeries.com/location/index.htm', 'http://www.snaap.org.uk/leisure-provider-directory.shtml', 'http://www.snlonline.net/Prospects/program_info.asp', 'http://www.smithevents.com/', 'http://www.smithslandingapartments.com/contact.asp', 'http://www.smithslandingapartments.com/faq.php', 'http://www.smhsknights.org/fieldhockeygamereports.htm', 'http://www.snowyrangegraphics.com/Links.html', 'http://www.smpcorp.com/Default.aspx', 'http://www.snocoblueprint.org/accomplishments.html', 'http://www.snocoblueprint.org/agribusiness/agribusiness.html', 'http://www.smith-wesson-scope-mount.com/home.html', 'http://www.smasher.fr/pages/smasher.html', 'http://www.smokefreecolorado.com/index.aspx', 'http://www.smokefreecolorado.com/resources.aspx', 'http://www.snaptive.com/index.html', 'http://www.smileshop.com.au/comfort.html', 'http://www.smokeysoutdoors.com/SCRIPTS/contactUs.asp', 'http://www.smokeysoutdoors.com/SCRIPTS/default.asp', 'http://www.snp-y.org/', 'http://www.smsmt.com/About-SMS.aspx', 'http://www.smsmt.com/About-SMS/Investors.aspx', 'http://www.sncs.org/grass-valley-family.htm', 'http://www.snow-guide.com/conditions.cfm/vt07.htm', 'http://www.smchsband.org/', 'http://www.smithdiving.com/newsevents/event_pum.html', 'http://www.smithdiving.com/newsevents/faq_scb.html', 'http://www.snakeoilproductions.com/airbrush.html', 'http://www.snakeoilproductions.com/index.html', 'http://www.smokingfetishglamour.com/', 'http://www.sncs.org/employment.htm', 'http://www.smxrtos.com/articles/rtoslic.htm', 'http://www.smdep.org/transexceptions.htm', 'http://www.snaap.org.uk/snaapies.shtml', 'http://www.snowwhite.ch/e/mobile_log.htm', 'http://www.smileshop.com.au/dentist-tour3.html', 'http://www.snipclip.com/snipclip/company.aspx', 'http://www.snorkelgrenada.com/about-grenada.htm', 'http://www.smithnsmith.com/index.php', 'http://www.snackaisle.com/page/S/CTGY/AN', 'http://www.snackaisle.com/page/S/CTGY/BOSTON', 'http://www.smxrtos.com/articles/mlcslc.htm', 'http://www.smolyan.a-bulgaria.com/it/', 'http://www.smolyan.a-bulgaria.com/', 'http://www.snorkelgrenada.com/Dive-Shows.htm', 'http://www.snow-guide.com/eventad.cfm/co12/39152.htm', 'http://www.smps.us/links2.html', 'http://www.sms4smiles.com/diwali-sms/sukh-ki-barsat-happy-deepawali.html', 'http://www.smartwebby.com/DreamweaverTemplates/templates/business_telecom_template71.asp', 'http://www.smartwebby.com/DreamweaverTemplates/templates/business_general_template59.asp', 'http://www.snipclip.com/snipclip/community/news/tabid/55/Default.aspx', 'http://www.smokeymountains.net/accommodations/getList/', 'http://www.smcancercenter.org/about_physicians/', 'http://www.smsmalls.co.za/gateway.asp', 'http://www.smpdesigns.co.uk/', 'http://www.smoothdraw.com/product/sd_help/sd3help.htm', 'http://www.smilesmadeeasy.com/', 'http://www.snowyrangegraphics.com/Contact_Sam.html', 'http://www.smps.us/Unitrode2.html', 'http://www.snowpilot.org/', 'http://www.snhc.com/yummyshakes.htm', 'http://www.snaptive.com/gallery/', 'http://www.smooth-transition.com/index.html', 'http://www.snakewhip.com/', 'http://www.smfg.co.jp/english/aboutus/profile/smbcfriend_history.html', 'http://www.snowdirt.com/index.html', 'http://www.smithworkz.com/football.htm', 'http://www.snips.8m.com/home.htm', 'http://www.snips.8m.com/fsguest.html', 'http://www.smcancercenter.org/cancer/breast/', 'http://www.smithevents.com/Sylvia-Browne-Ireland-2009/Note', 'http://www.smileandactnice.com/home/growingpains/devilsivy/index.html', 'http://www.smokeymountains.net/eventcalendar/event/55', 'http://www.smdep.org/progsites/yale', 'http://www.smsmalls.co.za/content_main.asp', 'http://www.smpcorp.com/main/CompanyPresentations.aspx', 'http://www.smithminerals.com/', 'http://www.snowboardinglatest.com/partners/', 'http://www.smithlawgroup.net/', 'http://www.smithauctionservices.com/', 'http://www.snlonline.net/Prospects/Prospect_faq.asp', 'http://www.smileandactnice.com/home/handygirl/nickoftime/index.html', 'http://www.smfg.co.jp/english/aboutus/profile/smbc_history.html']
