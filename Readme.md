

## AppUI Instructions:

  ### Constructor
**AppUI**(title, features, logo="logo.png", logo_width=300, logo_height=181)

- **title**: Application Window title

- **features**: Features dictionary in the followinf format:

    {

	"file1.txt":["Test1","Test2","Test3"],

	"file2.txt":["Test4","Test5","Test6"],

	"file3.txt":["Test7","Test8","Test9"],

	(...)

	}

- **logo**: Path to the logo file. (Default: ./logo.png)

- **logo_width**: The logo width. (Default: 300px)

- **logo_height**: The logo height. (Default: 181px)

### Updating progress from another process
You need to use the shared_memory block called "APPUI_WINDOW" for this.
Simply do:
```python
	from multiprocessing import shared_memory

	smh = shared_memory.SharedMemory(name="APPUI_WINDOW")
	buffer = smh.buf
	buffer[0] = 0 # Current progress from 0 to 100
	buffer[1:79] = b'sup boooy' # Process string (max 79 characters)
	buffer[80] = 0 # 1 - Screen Active, 0 - Screen Inactive
```


### Methods

##
#### minimize()

Minimize the app screen.
##

#### maximize()
Maximize the app screen.
##

#### check_all()
Check all checkboxes.
##

#### uncheck_all()
Uncheck all checkboxes.
##

#### get_selected()
Returns a list of all selected checkboxes. Returns an empty list if none is selected.
##

#### next_page()
Go to the next page of checkboxes.
##

#### previous_page()
Go to the previous page of checkboxes.
##

#### set_confirm_command(function)
Set what function will be called when "Confirm" button is pressed.
 - **function**: The function that will be called when "Confirm" button is pressed.
##

#### set_results_command(function)
Set what function will be called when "Results" button is pressed.
 - **function**: The function that will be called when "Results" button is pressed.
##

#### update_progress(progress)
Updates the current progressbar's progress.
 - **progress**: Current progress to be assigned to the progressbar. **(0 - 100)**
##

#### update_process(process)
Updates the current process shown above the progress bar.
 - **process**: Process name to show above the progress bar
##

#### reset_progress()
Clears the process text and zeroes the progressbar.
##

#### is_test_selected()
Returns **"True"** if any test is selected of **"False"** otherwise.
##

#### show_popup(title, message)
Shows a popup above the main app screen.
 - **title**: The popup window title.
 - **message**: The message to be shown.
##

#### disable_screen()
Disable all butons and checkboxes, preventing clicks.
##


#### enable_screen()
Enable all butons and checkboxes, allowing clicks.


