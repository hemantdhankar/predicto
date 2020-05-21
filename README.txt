 PredictO
*****************
We have made this website on django. Please read the instructions given below carefully and install each dependency.

Dependencies
************
~Python3

~Python packages (install via pip):
	django version 2.0.2
	matplotlib
	email
	selenium
	html
	multiprocessing

~ Other Drivers & Tools
	Install Mozilla Firefox
	Download Firefox driver (geckodriver.exe)(Place in the "predicto/predicto-project" and "predicto/predicto-project/predicto/" directories)
	NOTE: you must download geckodriver according to your PC configuration and replace the existing one.

~ A GOOD INTERNET CONNECTION IS MUST. YOU MAY NOT RECIEVE RESULTS IF YOUR CONNECTION IS WEAK OR INTERRUPTED IN MIDDLE OF THE CODE EXECUTION.

~ DO NOT CHANGE THE CODE WHILE YOUR RESULT IS BEING PREPARED. DOING SO MIGHT RESULT IN CANCELLATION OF YOUR TASK.

HOW TO RUN THE SERVER?
**********************
1) After installing all above dependencies. Go to the directory "predicto/predicto-project/" in your terminal. (You should see manage.py file there) 

2) RUN: 	python manage.py runserver	(python3 if you are using linux)

3) The server is now running at http://127.0.0.1:8000/

4) Open browser and open the link given in step 3. (Or you can type localhost:8000)

5) Enter your name, email, upload the sequence file and hit Submit!

DONE. Now you will recieve email with the results. 