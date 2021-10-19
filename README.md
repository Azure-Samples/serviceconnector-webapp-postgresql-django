# Tutorial: Connect a WebApp to Azure Database for PostgreSQL with Service Connector
Using the Azure portal, you can deploy a data-driven Python Django web app to Azure App Service and connect it to an Azure Database for PostgreSQL database. You can start with a free pricing tier that can be scaled up at any later time. 
In this tutorial, you use the Azure portal to complete the following tasks: 

- Provision a web app in Azure that deploys from a GitHub repo 

- Provision a PostgreSQL server and database in Azure and connect it to the web app. 

- Connect the web app and PostgreSQL server with Service Connector
  
- Automatically deploy from GitHub and validate connection result. 

## 1. Prepare

**Fork** the repository into your own GitHub account. 

You create a fork of this repository so you can make changes and redeploy the code in a later step. 


## 2. Provision the web app in Azure 

Provision the web app in Azure 

- Open the Azure portal

- Select Create a resource, which opens the New page. 

- Search for and select Web App, then select Create. 

- On the Create Web App page, enter the following information: 

|  Field   | Value  |
|  ----  | ----  |
| Subscription  | Select the subscription you want to use if different from the default. (Select “Resource Connector Test” if you are using the test subscription from the project team)  |
| Resource group   | Select Create new and enter "DjangoPostgres-Tutorial-rg".  |
| App name   | A name for your web app that's unique across all Azure (the app's URL is `https://<app-name>.azurewebsites.net`). Allowed characters are A-Z, 0-9, and -. A good pattern is to use a combination of your company name and an app identifier. |
|  Publish | Select Code.  |
| Runtime stack   | Select Python 3.8 from the drop-down list. |
|  Region | Select East US.  |
|  Linux Plan  | The portal will populate this field with an App Service Plan name based on your resource group. If you want to change the name, select Create new.  |
|  Sku and size  | For best performance, use the default plan, although it incurs charges in your subscription. To avoid charges, select Change size, then select Dev/Test, select B1 (free for 30 days), then select Apply. You can scale the plan later for better performance.  |

- Select Review + Create, then select Create. Azure takes a few minutes to provision the web app. 

- After provisioning is complete, select Go to resource to open the overview page for the web app. Keep this browser window or tab open for later steps. 

## 2. Provision the PostgreSQL database server in Azure 

- Open a new browser window or tab with the Azure portal (Please use this link). You use a new tab for provisioning the database because you'll need to transfer some information from the database page to the web app page still open from the previous section. 

- Select Create a resource, which opens the New page. 

- Search for and select Azure Database for PostgreSQL, then select Create. 

- On the next page, select Create under Single server. 

- On the Single server page, enter the following information: 

|  Field   | Value  |
|  ----  | ----  |
| Subscription  | Select the subscription you want to use if different from the default. (Select “Resource Connector Test” if you are using the test subscription from the project team)   |
| Resource group   | Select the "DjangoPostgres-Tutorial-rg" group you created in the previous section.   |
| Server name   |  A name for the database server that's unique across all Azure (the database server's URL becomes https://<server-name>.postgres.database.azure.com). Allowed characters are A-Z, 0-9, and -. A good pattern is to use a combination of your company name and and server identifier.  |
| Data source   |  None |
| Location  |  Select a location near you.  |
|  Version |  Keep the default (which is the latest version).  |
| Compute + Storage   |  Select Configure server, then select Basic and Gen 5. Set vCore to 1, set Storage to 5GB, then select OK. These choices provision the least expensive server available for PostgreSQL on Azure. You might also have credit in your Azure account that covers the cost of the server.  |
|  Admin username, Password, Confirm password  |  Enter credentials for an administrator account on the database server. Record these credentials as you'll need them later in this tutorial. Note: do not use the `$` character in the username or password. Later you create environment variables with these values where the `$` character has special meaning within the Linux container used to run Python apps.  |


- Select Review + Create, then Create. Azure takes a few minutes to provision the web app. 

- After provisioning is complete, select Go to resource to open the overview page for the database server. 


## 3. Create the pollsdb database on the PostgreSQL server 

In this section, you connect to the database server in the Azure Cloud Shell and use a PostgreSQL command to create a "pollsdb" database on the server. This database is expected by the sample app code. 

From the overview page for the PostgreSQL server, select select Connection security (under Settings on the left side). 

Portal connection security page for firewall rules 

Select the button labeled Add `0.0.0.0 - 255.255.255.255`, then select Continue in the pop up message that appears, followed by Save at the top of the page. These actions add a rule that allows you to connect to the database server from the Cloud Shell as well as SSH (as you do in a later section to run Django data model migrations). 

Open the Azure Cloud Shell from the Azure portal by selecting the Cloud Shell icon at the top of the window: 

Cloud Shell button on the Azure portal toolbar 

In the Cloud Shell, run the following command: 

```
psql --host=<server-name>.postgres.database.azure.com --port=5432 --username=<user-name>@<server-name> --dbname=postgres 
```

Replace `<server-name> and <user-name>` with the names used in the previous section when configuring the server. Note that the full username value that's required by Postgres is `<user-name>@<server-name>`. 

You can copy the command above and paste into the Cloud Shell by using a right-click and then selecting Paste. 

Enter your administrator password when prompted. 

When the shell connects successfully, you should see the prompt postgres=>. This prompt indicates that you're connected to the default administrative database named "postgres". (The "postgres" database isn't intended for app usage.) 

At the prompt, run the command ```CREATE DATABASE pollsdb;```. Be sure to include the ending semicolon, which completes the command. 

If the database is created successfully, the command should display CREATE DATABASE. To verify that the database was created, run \c pollsdb. This command should change the prompt to pollsdb=>, which indicates success. 

Exit psql by running the command exit. 

## 4. Deploy app code to the web app from a repository 
With the database and connection settings in place, you can now configure the web app to deploy code directly from a GitHub repository. 

- In the browser window or tab for the web app, select Deployment Center (under Deployment on the left side). 

- In the **Source**, select **GitHub** and then **Authorize** (if necessary). Then follow the sign-in prompts or select Continue to use your current GitHub login. Make sure you are **building with Github Actions**. 
If you see a popup window that says authentication succeeded, but the portal still shows the Authorize button, refresh the page and your GitHub login should appear in the GitHub box. Select the GitHub box again, then select Continue. 

- In the Github and Build section, select the following values: 

|  Field   | Value  |
|  ----  | ----  |
| Organization  | The GitHub account to which you forked the sample repository.  |
| Repository  |  serviceconnector-webapp-postgresql-django |
| Branch  |  main |
| Runtime stack   |  Python |
| Version   |  Python 3.8  |
 
 
- Select Save. Azure should deploy the code within a few seconds and start the app. 
App Service detects a Django project by looking for a wsgi.py file in each subfolder. When App Service finds that file, it loads the Django web app. For more information, see Configure built-in Python image. 

## 5. Connect the database 

With the code deployed and the database in place, the next step is to connect your app service to the database. In this section, you create settings for the web app that it needs to connect to the pollsdb database. These settings appear to the app code as environment variables. (For more information, see Access environment variables.) 

Switch back to the browser tab or window for the web app you created in a previous section. 

Select Configuration (under Settings on the left side), then select Resource Connector at the top of the page. (If you cannot see the Resource Connector button, please use this link) 

Use the Resource Connection button to create a connection. Each connection will generate a set of settings in the Application settings (which are expected by the djangoapp sample). Select the following values (Please make sure you use DB as the connection name): 

|  Field   | Value  |
|  ----  | ----  |
| Connection name   | DB  |
| Service type | Azure Database for PostgreSQL server |
| Subscription  | Select the subscription you are using when creating the PostgreSQL server   |
| Client Type | Django |
| Postgres Server  | Your Postgres server name  |
| Postgres database  | pollsdb  |
| Authentication type   | Connection string  |
| Username  | username  |
| Password  | password  |

- Click Save. It might take a few seconds to save your connection. Upon successful connection, 4 new application settings are added. 

  - AZURE_POSTGRESQL_HOST 

  - AZURE_POSTGRESQL_NAME 

  - AZURE_POSTGRESQL_PASSWORD 

  - AZURE_POSTGRESQL_USER 

- To check connection status, click validate button.


## 6. Run Django database migrations 

The only piece that remains is to establish the necessary schema in the database itself. You do this by "migrating" the data models in the Django app to the database. 

In the browser window or tab for the web app, select SSH (under Development Tools on the left side), and then Go to open an SSH console on the web app server. It may take a minute to connect for the first time as the web app container needs to start. 

In the console, change into the web app's folder: 

```
cd $APP_PATH 
```

Activate the virtual environment: 
```
source /pythonenv3.8/bin/activate 
```
Install dependencies: 
```
pip install -r requirements.txt 
```
Run database migrations: 
```
python manage.py migrate 
```
If you encounter any errors related to connecting to the database, check the values of the pip install -r rapplication settings created in Connect the database. 

Create an administrator login for the app: 
```
python manage.py createsuperuser 
```
The createsuperuser command prompts you for Django superuser (or admin) credentials, which are used within the web app. For the purposes of this tutorial, use the default username root, press Enter for the email address to leave it blank, and enter Pollsdb1 for the password. 

## 7. Create a poll question in the app 

You're now ready to run a quick test of the app to demonstrate that it is working with the PostgreSQL database. 

- In the browser window or tab for the web app, return to the Overview page, then select the URL for the web app (of the form `http://<app-name>.azurewebsites.net`). 

- The app should display the message "Polls app" and "No polls are available" because there are no specific polls yet in the database. 

- Browse to `http://<app-name>.azurewebsites.net/admin` (the "Django Administration" page) and sign in using the Django superuser credentials from the previous section (root and Pollsdb1). 

- Under Polls, select Add next to Questions and create a poll question with some choices. 

- Browse again to `http://<app-name>.azurewebsites.net/` to confirm that the questions are now presented to the user. Answer questions however you like to generate some data in the database. 

**Congratulations!** You're running a Python Django web app in Azure App Service for Linux, with an active PostgreSQL database. 

## 8. Clean up resources  

The resource you created in this tutorial (App Service and PostgreSQL database) takes ~100USD/month. If you'd like to keep the app or continue to the additional tutorials, skip this section. To avoid incurring ongoing charges, Otherwise, to avoid incurring ongoing charges you can delete the resource group create for this tutorial: 

- On the Azure portal, enter "DjangoPostgres-Tutorial-rg" in the search bar at the top of the window, then select the same name under Resource Groups. 

- On the resource group page, select Delete resource group. 

- Enter the name of the resource group when prompted and select Delete. 