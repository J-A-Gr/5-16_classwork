1. ✔ Create a second registration step that users must complete after the initial email and password registration:
   Update User Database Model:
   Add additional fields(or create other table) for user profile information (name, date of birth, phone, etc.)
2. ✔ Create Second Registration Step Route:
   Define a route "/register/step2" that is only accessible after initial registration
3. ✔ Create Second Registration HTML Template:
   Design "register_step2.html" with form fields for additional user information
   Include navigation controls (back/submit buttons)
4. ✔ Implement Second Step Form Processing:
   Add form validation for the additional fields
   Update the user record with the additional information upon submission
   Display "Registration complete" upon successful completion of both steps
5. ✔ Modify Initial Registration Flow:
   Update the first registration step to redirect to second step instead of showing success message
