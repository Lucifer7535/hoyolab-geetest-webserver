# Hoyolab-Geetest-Webserver

This project serves as a web server for enabling users to set up Geetest captcha verification for the [Genshin Discord Bot](https://github.com/Lucifer7535/Genshin-Discord-Bot). Therefore, this project tightly integrates with the database operations of the Genshin Discord Bot. If you need to develop and test independently, please remove the code related to the database.

### Workflow
1. **Genshin Discord Bot:**
    1. Triggers the Hoyolab verification request and receives `gt` and `challenge` from Hoyolab.
    2. Generates a link for users to connect to this web server.
2. **This Program:**
    1. Receives user `discord_id`, `gt`, and `challenge` through URL GET paths.
    2. Generates a webpage and returns it to the user, with JavaScript initiating the captcha verification.
    3. After the user unlocks the captcha verification, the Geetest server returns `challenge`, `validate`, and `seccode`.
    4. Sends a POST request to this program with the data from step 2.3. This program receives and saves it to the database.
