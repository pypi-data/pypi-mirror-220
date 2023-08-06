from ...base.firebase_collection import FirebaseCollectionBase, getTimestamp
from ....utils import (DictUtils, get_object_model_class, init_class_kwargs, Crypto)
from ....utils.response import ApiResponse, Error, ResponseStatus, StatusCode
from .user_fields import UserFields, UserFieldProps, STANDARD_FIELDS, USERS_COLLECTION
from typing import List
from typing import Any
from dataclasses import dataclass
from firebase_admin import auth as admin_auth
from adafri.v1.auth.firebase_auth import create_firebase_user
from firebase_admin.exceptions import FirebaseError
import pydash

@dataclass
class Account:
    canManageClients: bool
    childs: List[object]
    currenyCode: str
    customerId: int
    dateTimeZone: str
    name: str
    testAccount: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        _canManageClients = DictUtils.pick(obj, "canManageClients", bool)
        _childs = [y for y in DictUtils.pick(obj, "childs", list)]
        _currenyCode = str(DictUtils.pick(obj, "currenyCode", str))
        _customerId = int(DictUtils.pick(obj, "customerId", int))
        _dateTimeZone = str(DictUtils.pick(obj, "dateTimeZone",str))
        _name = str(DictUtils.pick(obj, "name", str))
        _testAccount = bool(DictUtils.pick(obj, "testAccount", bool))
        return Account(_canManageClients, _childs, _currenyCode, _customerId, _dateTimeZone, _name, _testAccount)

@dataclass
class Country:
    areaCodes: List[object]
    dialCode: str
    flagClass: str
    htmlId: str
    iso2: str
    name: str
    placeHolder: str
    priority: int

    @staticmethod
    def from_dict(obj: Any) -> 'Country':
        _areaCodes = [y for y in DictUtils.pick(obj, "areaCodes", list)]
        _dialCode = str(DictUtils.pick(obj, "dialCode", str))
        _flagClass = str(DictUtils.pick(obj, "flagClass",str))
        _htmlId = str(DictUtils.pick(obj, "htmlId", str))
        _iso2 = str(DictUtils.pick(obj, "iso2", str))
        _name = str(DictUtils.pick(obj, "name", str))
        _placeHolder = str(DictUtils.pick(obj, "placeHolder", str))
        _priority = int(DictUtils.pick(obj, "priority", int))
        return Country(_areaCodes, _dialCode, _flagClass, _htmlId, _iso2, _name, _placeHolder, _priority)

@dataclass
class Credential:
    refresh_token: str
    scopes: List[str]
    token: str
    token_uri: str

    @staticmethod
    def from_dict(obj: Any) -> 'Credential':
        _refresh_token = str(DictUtils.pick(obj, "refresh_token", str))
        _scopes = [y for y in DictUtils.pick(obj, "scopes", list)]
        _token = str(DictUtils.pick(obj, "token", str))
        _token_uri = str(DictUtils.pick(obj, "token_uri", str))
        return Credential(_refresh_token, _scopes, _token, _token_uri)

@dataclass
class DeviceInfo:
    browser: str
    browser_version: str
    device: str
    os: str
    os_version: str
    userAgent: str

    @staticmethod
    def from_dict(obj: Any) -> 'DeviceInfo':
        _browser = str(DictUtils.pick(obj, "browser", str))
        _browser_version = str(DictUtils.pick(obj, "browser_version", str))
        _device = str(DictUtils.pick(obj, "device", str))
        _os = str(DictUtils.pick(obj, "os", str))
        _os_version = str(DictUtils.pick(obj, "os_version", str))
        _userAgent = str(DictUtils.pick(obj, "userAgent", str))
        return DeviceInfo(_browser, _browser_version, _device, _os, _os_version, _userAgent)

@dataclass
class PartenerData:
    id: str
    text: str

    @staticmethod
    def from_dict(obj: Any) -> 'PartenerData':
        _id = str(DictUtils.pick(obj, "id", str))
        _text = str(DictUtils.pick(obj, "text", str))
        return PartenerData(_id, _text)

@dataclass
class PhoneInfo:
    countryCode: str
    dialCode: str
    e164Number: str
    internationalNumber: str
    nationalNumber: str
    number: str

    @staticmethod
    def from_dict(obj: Any) -> 'PhoneInfo':
        _countryCode = str(DictUtils.pick(obj, "countryCode", str))
        _dialCode = str(DictUtils.pick(obj, "dialCode", str))
        _e164Number = str(DictUtils.pick(obj, "e164Number", str))
        _internationalNumber = str(DictUtils.pick(obj, "internationalNumber", str))
        _nationalNumber = str(DictUtils.pick(obj, "nationalNumber", str))
        _number = str(DictUtils.pick(obj, "number", str))
        return PhoneInfo(_countryCode, _dialCode, _e164Number, _internationalNumber, _nationalNumber, _number)

@dataclass
class PlateformRole:
    id: str
    partenerData: PartenerData
    text: str

    @staticmethod
    def from_dict(obj: Any) -> 'PlateformRole':
        _id = str(DictUtils.pick(obj, "id", str))
        _partenerData = PartenerData.from_dict(DictUtils.pick(obj, "partenerData", dict))
        _text = str(DictUtils.pick(obj, "text", str))
        return PlateformRole(_id, _partenerData, _text)


@dataclass(init=False)
class User(FirebaseCollectionBase):
    account_value: int = None;
    accounts: List[Account]
    addresse: str
    auth_code: str
    authorizedPush: bool
    country: Country
    credentials: List[Credential]
    deviceInfo: DeviceInfo
    displayName: str
    email: str
    entrepriseName: str
    entrepriseUrl: str
    first_name: str
    hasApprouvedPolicy: bool
    invitedAccounts: List[object]
    isConnectWithMailAndPassword: bool
    isCorporate: bool
    isDesktopDevice: bool
    isMobile: bool
    isParticular: bool
    isTablet: bool
    last_name: str
    linkedAccounts: List[object]
    ownedAccounts: List[object]
    phoneInfo: PhoneInfo
    photoURL: str
    plateformRole: PlateformRole
    postal: str
    profileCompleted: bool
    showPushToken: bool
    telephone: str
    token: List[str]
    uid: str
    user_type: str
    password: str
    provider: str
    
    def __init__(self, user=None, **kwargs):
        (cls_object, keys, data_args) = init_class_kwargs(self, user, STANDARD_FIELDS, UserFieldProps, USERS_COLLECTION, ['id','uid'], **kwargs)
        super().__init__(**data_args);
        for key in keys:
            setattr(self, key, cls_object[key]);
    


    @staticmethod
    def generate_model(_key_="default_value"):
        user = {};
        props = UserFieldProps
        for k in DictUtils.get_keys(props):
            user[k] = props[k][_key_];
        return user;

    @staticmethod
    def from_dict(user: Any, db=None, collection_name=USERS_COLLECTION) -> 'User':
        cls_object, keys = get_object_model_class(user, User, UserFieldProps);
        _user = User(cls_object, db=db, collection_name=collection_name)
        return _user
    
    def get(self):
        doc = self.document_reference().get();
        if doc.exists is False:
            return None;
        return User.from_dict(doc.to_dict(), db=self.db, collection_name=self.collection_name);

    def query(self, query_params: list, first=False, limit=None):
        result = [];
        query_result = self.custom_query(query_params, first=first, limit=limit)
        if bool(query_result):
            if first:
                return User.from_dict(user=query_result, db=self.db, collection_name=self.collection_name)
            else:
                for doc in query_result:
                    result.append(User.from_dict(user=doc, db=self.db, collection_name=self.collection_name))
                return result
        if first:
                return None
        return [];

    def create(self, **kwargs):
        data_dict = DictUtils.pick_fields(kwargs, UserFields.filtered_keys('mutable', True));
        user_model = User().from_dict(DictUtils.merge_dict(data_dict, User.generate_model()));
        if bool(user_model.to_json()) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Empty request","INVALID_REQUEST", 1)).to_json(), 200
        
        email = user_model.email
        password = user_model.password
        
        if bool(email) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Email required","INVALID_REQUEST", 1));
    
        if bool(password) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Password required","INVALID_REQUEST", 1));
    
        docs = User().collection().where('email', '==', email).get();
        found_users = [];
        if len(docs) > 0:
            for doc in docs:
                found_users.append(User.from_dict(doc.to_dict()).to_json());
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"User wiith emaill {user_model.email} already exist","INVALID_REQUEST", 1));
    
    
        try:
            user_model.isConnectWithMailAndPassword = bool(user_model.uid) is False
            if bool(user_model.uid) is False:
                user_record = create_firebase_user(email, password);
                user_model.uid = user_record.uid;
                hashed_password = Crypto().encrypt(password);
                user_model.password = hashed_password;
            User().collection().document(user_model.uid).set({**user_model.to_json(), "createdAt": getTimestamp()}, merge=True)
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, user_model.to_json(), None);
        except Exception as e:
            print(e)
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(str(e),"INVALID_REQUEST", 1));
    
    def update(self, data):
        try:
            last_value = self.to_json();
            filtered_value = pydash.pick(data, UserFields.filtered_keys('editable', True));
            new_value = DictUtils.merge_dict(filtered_value, self.to_json());
            changed_fields = DictUtils.get_changed_field(last_value, new_value);
            data_update = DictUtils.dict_from_keys(filtered_value, changed_fields);
            if bool(data_update) is False:
                return None;
            self.document_reference().set(data_update, merge=True)
            return DictUtils.dict_from_keys(self.get().to_json(), changed_fields);
        except Exception as e:
            print(e)
            return None;

    def remove(self, only_mark_as_removed=True):
        try:
            if self.id is None:
                return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Cannot identify User with id {self.id}","INVALID_REQUEST", 1));
            if only_mark_as_removed:
                self.document_reference().set({"is_removed": True})
            else:
                self.document_reference().delete();
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, {"message": f"User {self.id} deleted"}, None);
        except:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"An error occurated while removing authorization code with id {self.id}","INVALID_REQUEST", 1));

    
    def get_firebase_user(self, key: str, value: str) -> 'admin_auth.UserRecord':
        try:
            if key == 'email':
                return admin_auth.get_user_by_email(value)
            elif key == 'uid':
                return admin_auth.get_user(value)
            elif key == 'phone':
                return admin_auth.get_user_by_phone_number(value)
        except ValueError as e:
            raise e
        except FirebaseError as e:
            raise e;    
        except admin_auth.UserNotFoundError as e:
            raise e;  


