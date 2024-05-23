# telegram-event-publisher

This project integrates Google Calendar with Telegram, notifying users of their upcoming events for the month.

## Prerequisites

### Connect To Google Calendar Using A Service Account

Before continuing, make sure you have a Google Account.

#### Project Creation

* Go to the [Google Cloud Console](https://console.cloud.google.com/).
* Click on the project drop-down and then click on NEW `PROJECT`.
* Give your project a name and click `CREATE`.

#### Enable Google Calendar API

* In the left sidebar, navigate to `APIs & Services` > `Library`.
* Search for `Google Calendar API` and select it.
* Click `ENABLE`.

#### Service Account Creation

* In the left sidebar, navigate to `IAM & Admin` > `Service accounts`.
* Click on `CREATE SERVICE ACCOUNT`.
* Provide a name and description for the service account. Click `CREATE`.
* Grant the service account the required permissions. For basic calendar access, you can choose `Role` > `Google Calendar API` > `Calendar Viewer`. Click `CONTINUE`.
* Click `DONE`.

#### Download Credentials

* In the service accounts list, find the service account you just created.
* Click on its name to view details.
* In the `KEYS` tab, click on `ADD KEY` > `JSON`.
* A `credentials.json` file will be downloaded. This file contains the credentials your application will use to authenticate its API requests.

#### Share Your Google Calendar

If you're intending to access a specific Google Calendar, make sure to share it with your service account:

* Open [Google Calendar](https://calendar.google.com/).
* Next to your calendar's name, click on the three dots and choose `Settings and sharing`.
* Scroll to the `Share with specific people`` section.
* Click on `+ Add people` and enter the email address of the service account (found in the service account details in Google Cloud Console).
* Set the desired permissions (e.g., `See all event details`) and click `Send`.

### Telegram Bot Token and Channel ID

* [Telegram Bot Tutorial](https://core.telegram.org/bots/tutorial).

## Configuration

* Google Calendar:
  * credentials.json

* Telegram:
  * Environment Tokens.

## Customization

* Event Formatting:
  * Modify the monthly_events_template.txt found in the templates directory to adjust the appearance of event messages.
* Extended Fields in Google Calendar:
  * When creating events in Google Calendar, you can specify additional details in the description as follows:

```txt
Tickets: [Ticket Info]
Location: [Location Info]
Website: [Website URL]
```

The application will parse these details and include them in the Telegram message.

## Local Development

### Prerequisites

* **This project requires [Python 3.11](https://www.python.org/downloads/release/python-3113/).**

* Dependencies are managed using [Poetry](https://python-poetry.org/docs/#installation). If you haven't installed it yet, use this command:

    ```shell
    pip install poetry
    ```

* [Pre-commit](https://pre-commit.com/) is used to enforce code quality. If you don't have pre-commit installed, you can install it using the following command:

  ```shell
  pip install pre-commit
  ```

### Setting up the Development environment

1. Initialize pre-commit:

    ```shell
    pre-commit install
    ```

2. Install dependencies and activate the virtual environment:

    ```shell
    poetry install --no-root
    ```

3. The following Environment Variables must exist locally to run this project.

    * `GOOGLE_CALENDAR_ID` - The ID of the calendar that is to be read from.
        * Go to [Google Calendar](https://calendar.google.com/).
        * Choose a Calendar:
            * On the left side of the page, you'll see a section titled `My calendars.` These are the calendars associated with your account.
            * Hover over the name of the calendar you're interested in. When you do, you'll notice three vertically aligned dots appear to the right of the calendar's name. This is the `Options` menu for that calendar.
        * Access Calendar Settings:
            * Click on the `Options` (three dots) next to the calendar name.
            * From the dropdown menu that appears, select `Settings and sharing`.
        * Find the Calendar ID:
            * In the settings page, scroll down to the “Integrate calendar” section.
            * Here, you'll find a field labeled `Calendar ID`. This is the ID you're looking for. It often looks like an email address and might end with @group.calendar.google.com.
    * `TELEGRAM_CHAT_ID`
    * `TELEGRAM_API`
    * `GOOGLE_CREDENTIALS`
        * Using the `crendentials.json` file downloaded as described in [Download Credentials](#download-credentials), store it's contents as an environment variable as shown below.

            ```sh
            export GOOGLE_CREDENTIALS=$(cat credentials.json)
            ```

## Refrences

* [Google Calendar API Python documention](https://developers.google.com/calendar/api/quickstart/python).
