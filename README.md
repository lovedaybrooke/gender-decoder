# gender-decoder

Gender Decoder is a simple  tool that checks the text of job ads to see if it includes any subtly gender-coded language. 

By 'subtly gender-coded language' I mean language that reflects stereotypes about men and women, like women being more nurturing and men more aggressive. A 2011 research paper showed that subtly masculine-coded language in ads can put women off applying for jobs.

To be clear: I don't believe that the concepts with masculine-coded words are the exclusive preserve of men. I know that people of all genders can be innovative, reckless, self-reliant and/or unreasonable. But the stereotype our society has created of men says that they are much more likely to have these qualities. The same thing goes for women. Unfortunately, people with non-binary genders were not included in the original research.

For more info, or to use the tool:
http://gender-decoder.katmatfield.com

The analysis bit of this tool has been made into a Python package, by Richard Pope:
https://pypi.python.org/pypi/genderdecoder

If you're interested in Gender Decoder, you may also like Karen Schoellkopf's
https://www.hiremorewomenintech.com


Adding a new language
---------------------

1. **Add a new file to the wordlists directory**
   
   This MUST contain the following:
   + language_name (a human-readable name, to be shown in the language dropdown)
   + language_code (only alphanumeric characters and underscores)
   + feminine_coded_words (a list of strings, which are all translations of the English feminine coded words)
   + masculine_coded_words (as for the feminine coded words)

   NB: in English, the coded words are given as 'stems' to save effort. So, for instance, "collab" in these lists will match "collaborate", "collaborator", "collaboratively" and so on. You may wish to do the same for your new wordlist, if this pattern is the same for the language in question.

   It MAY contain:
   + source (your name, of the names of who-ever is responsible for the translated wordlist)

   The file MUST be named the same as the language_code included in it.

2. **Update the __init__ file in the wordlists directory**

   Add the language code for your new wordlist to __all__, set in line 4

3. **Update the list of languages in the tests.py file**

   Add your new language to the test called test_language_field, in TestForms

4. **Run tests, and amend as necessary for a new language**

   I'd particularly suggest testing any new symbols or accented letters work as expected.

5. **Submit a pull request**

   You may prefer to fork the repo, but it'd be nice if we could offer your new language on the main site too.
   
   
## Install

One way is to run and develop using docker.

### Using docker-compose:

1. Build and start the container

    ```bash
   $ docker-compose up --build
   Building webapp
   Step 1/10 : FROM python:3
    ---> 59a8c21b72d4
   Step 2/10 : RUN pip install pipenv
    ---> Using cache
    ---> c0d5e3f85c38
   Step 3/10 : WORKDIR /app
    ---> Using cache
    ---> f3903c2620c1
   Step 4/10 : COPY ./Pipfile* /app/
    ---> Using cache
    ---> 9009b291fbd8
   Step 5/10 : RUN ls -l /app
    ---> Using cache
    ---> dbf81d3f73d1
   Step 6/10 : RUN pipenv install
    ---> Using cache
    ---> 1e74e10a79a9
   Step 7/10 : COPY . /app
    ---> 8b28935827d6
   Step 8/10 : EXPOSE 5000/tcp
    ---> Running in c2e32ae5708e
   Removing intermediate container c2e32ae5708e
    ---> 09a500bf31c7
   Step 9/10 : ENTRYPOINT ["pipenv", "run"]
    ---> Running in a3ef32804042
   Removing intermediate container a3ef32804042
    ---> 33bbc34d27b7
   Step 10/10 : CMD ["python", "runsite.py"]
    ---> Running in 88d8181ff056
   Removing intermediate container 88d8181ff056
    ---> 95f76f9c69f1
   Successfully built 95f76f9c69f1
   Successfully tagged gender-decoder_webapp:latest
   Recreating gender-decoder_webapp_1 ... done
   Attaching to gender-decoder_webapp_1
   webapp_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
   webapp_1  |  * Restarting with stat
   webapp_1  |  * Debugger is active!
   webapp_1  |  * Debugger pin code: 217-355-561
    ```
2. Open https://localhost:5000 in your browser

### Create the database

First make sure that the environment variable `DATABASE_URL` is correct.

```bash
export DATABASE_URL=postgres://katmatfield:Heartbleed@localhost/newdecoder
```

If not set it will default to a sqlite `app.db`. This will be fine for running locally but not great for running in multiple docker containers.

Create the database using docker-compose:

```bash
docker-compose run --rm webapp python db_create.py
```
