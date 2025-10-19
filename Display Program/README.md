# The display
This is the code for what you see on the website. To set it up:
- Rename .env.example to .env;
- Insert your NPSSO (found [here](https://ca.account.sony.com/api/v1/ssocookie), make sure to be logged in on the PlayStation website first) and your PSN ID;
- Install the required dependencies;
- Start the web server with:

```bash
flask --app app.dashboard run --debug --port 5001
```
