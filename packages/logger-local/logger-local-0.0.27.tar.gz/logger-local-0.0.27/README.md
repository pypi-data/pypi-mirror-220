# logger-local-python-package

# Initialize
run this command in the root directory of your project :

    pip install logger-local-python-package

# Import 
import instance from the package : 

from logger_local_python_package.localLogger import _Local_Logger as local_logger

# Usage
Note that you must have a .env file with the environment variables.

you can insert log into DB with 2 difference approach :

1. Writing a message :
    * local_logger.info("your-message");
    * local_logger.error("your-message");
    * local_logger.warn("your-message");
    * local_logger.debug("your-message");
    * local_logger.verbose("your-message");
    * local_logger.start("your-message");
    * local_logger.end("your-message");
    * local_logger.Init("your-message");
    * local_logger.exception("your-message");

2. Writing an object (Dictionary) :
    
   In case you have more properties to insert into the database,
   
   you can create a Dictionary object that contains the appropriate fields from the table and send it as a parameter.
   You can use local_logger.init if you want to save the fields for a few logging action. at the end please use clean_variables() function to clear those fields

   the Dictionary's keys should be the same as the table's columns names and the values should be with the same type as the table's columns types.

        objectToInsert = {
            'user_id': 1,
            'profile_id': 1,
            'activity': 'logged in the system',
            'payload': 'your-message',
        }

        local_logger.info(object=objectToInsert);
    
    None of the fields are mandatory.

3. Writing both object and message:
just use both former aproaches together as you can watch in here:
local_logger.info("your-message",object=objectToInsert);


Please add to requirements.txt<br>
replace the x with the latest version in pypi.org/project/logger-local<br>
logger-local==0.0.x <br>
<br>
Please include at least two Logger calls in each method:<br>
object1={
    arg1: arg1_value
    arg2: arg2_value
}
local_logger.start(object=object1)
object2={
    return: ret_value
}
local_logger.end(object=object2)

if you catch any exceptions please use:
exception exception as ex
local_logger.exception(object=e)

TOOD: We nee to add Unit Tests so this command will work<br>
python -m unittest .\tests\test_writer.py<br>


pip install -r .\requirements.txt<br>

To Run the tests (Not Unit Tests)<br>
python.exe .\tests\test_writer.py<br>