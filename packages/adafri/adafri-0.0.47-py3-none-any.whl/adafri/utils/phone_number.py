import phonenumbers



class PhoneNumber(object):
    def __init__(self, number, country_code=None):
        self.country_code = country_code
        self.number = phonenumbers.format_number(phonenumbers.parse(number, country_code), phonenumbers.PhoneNumberFormat.INTERNATIONAL);

    def parse(self,  country_code=None):
        try:
            c = country_code;
            if country_code is None:
                if self.country_code is not None:
                    c = self.country_code
            return phonenumbers.parse(self.number, c);
        except:
            return None;