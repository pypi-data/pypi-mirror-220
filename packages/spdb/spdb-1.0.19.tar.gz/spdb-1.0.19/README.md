# =====================================

# Sassy Python Database(and auth) utils

# =====================================

LICENSE: The MIT License


## Requirements

## ============

- Python 3.7 or higher
- pyotp
- qrcode
- setuptools


## Usage 

## =====

	import spdb

### Database

--------
	spdb.Database(path: str)  # Create Database object
	spdb.Database.create_tables(tables_names: list[str]) -> None  # Create tables if not exists
	spdb.Database.execute(code) -> str  # Execute sqlite3 code
	spdb.Database.read_json(name: str, data_id: str) -> dict  # Read data by ID as dict
	spdb.Database.read_object(Class: class, name: str, data_id: str) -> Class  # Read data by ID as object
	spdb.Database.write_json(name: str, data_id: str, data: dict) -> None  # Write dict by ID
	spdb.Database.write_object(name: str, object_id: str, object: Class) -> None  # Write object by ID
	spdb.Database.delete_dict(name: str, dict_id: str) -> None  # Delete dict by ID
	spdb.Database.delete_json(name: str, json_id: str) -> None  # Delete JSON by ID
	spdb.Database.delete_object(name: str, object_id: str) -> None  # Delete object by ID

	Static:
		spdb.Database.object_to_dict(object: Class) -> dict  # Convert object into dict
		spdb.Database.object_to_json(object: Class) -> dict  # Convert object into JSON-compatible dict
		spdb.Database.dict_to_object(Class: class, Dict: dict) -> Class  # Convert dict into object
		spdb.Database.dict_to_json(Dict: dict) -> dict  # Convert dict into JSON-compatible dict
		spdb.Database.json_to_object(Class: class, JSON: dict) -> Class  # Convert JSON into object

### TOTP - HOTP

-----------
	spdb.OTP(token: str=None, app_name: str=None)  # Create OTP object
	spdb.OTP.now() -> str  # Get TOTP code
	stdb.OTP.at(index: int) -> str  # Get HOTP code
	stdb.OTP.time_verify(code: str) -> bool  # Verify TOTP code
	stdb.OTP.counter_verify(index: int, code: str) -> bool  # Verify HOTP code
	stdb.OTP.TQR(name: str) ->  # Get TOTP QR-code for Google Authentificator
	stdb.OTP.HQR(name: str) ->  # Get HOTP QR-code for Google Authentificator

	Static:
		stdb.OTP.generate_token() -> str  # Generate random token

### Token Generator

---------------
	stdb.TokenGenerator(code: str)  # Create TokenGenerator object
	stdb.TokenGenerator.gen(type: str, ID: str, key: str) -> str  # Generate token

	Static:
		stdb.TokenGenerator.parse_token(token: str) -> dict  # Parse token

### Text Validator

--------------
	stdb.TextValidator(min: int=4, max: int=64, regexp: str=r'([A-z]|[0-9]|_|-)+')  # Create TextValidator object
	stdb.TextValidator.check(text: str) -> bool  # Check text for conditions

### Utils

-----
	stdb.utils.sha256(text: str) -> str  # Get sha256 from text
	stdb.utils.b32encode(text: str) -> str  # Encode str into base32 str
	stdb.utils.random_text(length: int=None) -> str  # Get random text
	stdb.utils.random_sha256() -> str  # Get random sha256 str
	stdb.utils.random_b32 -> str  # Get random base32 str

