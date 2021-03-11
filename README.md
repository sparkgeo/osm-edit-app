# osm-edit-app

A project for deploying the OSM Rails Port in a containerized environment.

## Local Environment

### Launching Containers

Standup the environment using the command:

```shell
docker-compose up --build
```

OSM can be access at `localhost:3000`. See the section below on next steps.

When you are done, shutdown the environment using the command:

```shell
docker-compose down
```

This will terminate the containers, but the volumes will persist. So the next time you `docker-compose up`, all you data will still be available.

> Note: Newest version of Docker Compose CLI (`docker-compose`) is used slightly different, such as `docker compose`. This is interchangable in the above examples.

### Next Steps

#### Create a User

Click on the `Sign Up` button in the top right of the home page (`localhost:3000`). Enter details as necessary. It is not confirgured to send emails, so you can use dummy values. This also means the user won't get activated. So to set the user as active, run the following commands:

```shell
docker exec -it osm-edit-app_web_1 /bin/bash
> bundle exec rails console
>> user = User.find_by_display_name("My Display Name")
>> user.status = "active"
>> user.save!
>> quite
> exit
```

Now when you go to `localhost:3000` you will be able to login appropriately.

#### Create a Oauth App

Now that you can login to the OSM UI, you still won't be able to click the edit button and open iD. You will need to create an Oauth App for this. Here are the steps copyied from the OSM docs: https://github.com/openstreetmap/openstreetmap-website/blob/master/CONFIGURE.md#oauth-consumer-keys.

Do the following:

* Log into your Rails Port instance, e.g. http://localhost:3000
* Click on your user name to go to your user page
* Click on "my settings" on the user page
* Click on "oauth settings" on the My settings page
* Click on 'Register your application'.
* Unless you have set up alternatives, use Name: "Local iD" and URL: "http://localhost:3000"
* Check the 'modify the map' box.
* Everything else can be left with the default blank values.
* Click the "Register" button
* On the next page, copy the "consumer key"
* Edit config/settings.local.yml in your rails tree
* Add the "id_key" configuration key and the consumer key as the value, ie:

```yaml
# Default editor
default_editor: "id"
# OAuth consumer key for iD
id_key: "8lFmZPsagHV4l3rkAHq0hWY5vV3Ctl3oEFY1aXth"
```

* Run `docker compose up --build`

You now can launch iD editor from the OSM UI via the edit button.

## Notes

* Ref for automating: https://github.com/openstreetmap/chef/blob/master/cookbooks/dev/templates/default/rails.setup.rb.erb
* When trying to save features, an error happens. Copying land.html from the iD repo under dist/ to the osm-website/public/ dir solves it for now.
* See the `.github/workflows` files for reference on how the base images are built.
