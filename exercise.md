Create a web application with login and register functionality for users to register and log in. The register page should feature an HTML form with email and password fields, while the login page should utilize a Flask WTF form with email and password fields. Upon successful registration, display "Successful registration". Upon successful login, display "Logged in successfully". On login failure, display "Incorrect email or password".

1. ✔ Define User Database Model:
   Create a User database model with the following attributes:
   id: Primary key
   email: Unique and not nullable string
   password: Not nullable string

2. ✔ Create Register Page:
   Define a route "/register" for the register page.
   Implement a function to handle GET and POST requests.
   On GET request, render the register template (register form).
   On POST request, handle registration form data.
   If registration is successful, return "Successful registration!" text.

3. ✔ Create Register HTML Template:
   Create a "register.html" template.
   Design the template to include a register form with:
   Email field
   Password field
   Submit button

4. ✔ Create Login Page:
   Define a route "/login" for the login page.
   Implement a function to handle GET and POST requests.
   On GET request, render the login template (login form).
   On POST request, handle login form data.
   If login is successful, return "Logged in successfully" text.
   If login fails, return "Invalid email or password" text. (Check if user with provided email and password exists)

5. ✔ Create Login HTML Template:
   Create a "login.html" template.
   Design the template to include a login form with:
   Email field
   Password field
   Submit button

6. Utilize Flask-WTF for Login Form:
   Create a Flask WTF form for the login page.
   Include email and password fields with required validations.

7. Implement Login Form Validations:
   Ensure that the email field has email and required validations.
   Ensure that the password field has a required validation.
