import phonenumbers

class PhoneNumber(object):
    number: str;
    national_number: str;
    international_number: str;
    dialCode: str;
    country_code: str;

    def __init__(self, number, country_code=None):
        parse = self.parse(number,country_code);
        if parse is not None:
            (
                self.number, self.national_number, 
                self.international_number, self.dialCode,self.country_code
            ) = parse

    def parse(self, _number, _country_code=None):
        try:
            number = _number
            country_code = _country_code;
            parsed = phonenumbers.parse(number, country_code);
            national_number = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL);
            international_number = phonenumbers.format_number(phonenumbers.parse(number, country_code), phonenumbers.PhoneNumberFormat.INTERNATIONAL);
            dialCode = parsed.country_code;
            if str(dialCode).split('')[0]!='+':
                dialCode = f"+{dialCode}"
            country_code = phonenumbers.region_code_for_country_code(parsed.country_code)
            return number, national_number,international_number,dialCode,country_code;
        except:
            return None;
    
    def to_json(self, _fields=None):
       return {
           "number": self.number,
           "national_number": self.national_number,
           "international_number": self.international_number,
           "dialCode": self.dialCode,
           "country_code": self.country_code
       }