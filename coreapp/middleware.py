CUSTOM_SECURE_EXPECT_CT = True
CUSTOM_SECURE_EXPECT_CT_MAX_AGE = 60 * 60 * 24 * 365  # 1 year
CUSTOM_SECURE_EXPECT_CT_ENFORCE = True
# CUSTOM_SECURE_EXPECT_CT_REPORT_URI = 'https://username.report-uri.com/r/d/ct/enforce'

class HeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        try:
            self.expect_ct = CUSTOM_SECURE_EXPECT_CT
        except AttributeError:
            self.expect_ct = False

    def __call__(self, request):
        response = self.get_response(request)

        if self.expect_ct:
            response['Expect-CT'] = self.__expect_ct_header_value()

        return response

    def __expect_ct_header_value(self):
        # logger = logging.getLogger(__name__)

        try:
            max_age = CUSTOM_SECURE_EXPECT_CT_MAX_AGE
        except AttributeError:
            max_age = 60 * 60 * 24  # 1 day
            print('CUSTOM_SECURE_EXPECT_CT setting is True but CUSTOM_SECURE_EXPECT_CT_MAX_AGE setting is not set. Default of %s applied.' % max_age)

        try:
            enforce = CUSTOM_SECURE_EXPECT_CT_ENFORCE
        except AttributeError:
            enforce = False
            print('CUSTOM_SECURE_EXPECT_CT setting is True but CUSTOM_SECURE_EXPECT_CT_ENFORCE setting is not set. Default of False applied.')

        # try:
        #     report_uri = CUSTOM_SECURE_EXPECT_CT_REPORT_URI
        # except AttributeError:
        #     report_uri = False
        #     print('CUSTOM_SECURE_EXPECT_CT setting is True but CUSTOM_SECURE_EXPECT_CT_REPORT_URI setting is not set. Default of False applied.')

        value = 'max-age=%s' % max_age

        if enforce:
            value += ', enforce'

        # if report_uri:
        #     value += ', report-uri="%s"' % report_uri

        return value