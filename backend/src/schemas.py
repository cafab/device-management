from marshmallow import Schema, fields, post_dump


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()

class PurchaseDetailsSchema(Schema):
    id = fields.Integer()
    supplier = fields.String(allow_none=True)
    price = fields.Decimal(as_string=True, allow_none=True)
    purchase_date = fields.Date(format="%d.%m.%Y", allow_none=True)
    notes = fields.String(allow_none=True)
    serial_number = fields.String()

class AccountsSchema(Schema):
    id = fields.Integer()
    current_account = fields.String()
    previous_account = fields.String(default="-")
    last_seen = fields.DateTime(format="%d.%m.%Y, %H:%M")
    serial_number = fields.String()

class ComputerSchema(Schema):
    serial_number = fields.String()
    computer_name = fields.String()
    ip_address = fields.String() 
    os = fields.String()
    os_install_date = fields.Date(format="%d.%m.%Y")
    computer_model = fields.String()
    cpu = fields.String()
    memory = fields.String()
    hard_disk = fields.String()
    purchase_details = fields.Nested(PurchaseDetailsSchema, many=True)
    accounts = fields.Nested(AccountsSchema, many=True)


