FROM sparkgeo/osm-rails-port:v0.7

ADD ./land.html /app/public/land.html
ADD ./database.yml /app/config/database.yml
ADD ./storage.yml /app/config/storage.yml
ADD ./settings.local.yml /app/config/settings.local.yml
ADD ./osm-db-functions.sql /app/config/osm-db-functions.sql
ADD ./init_db.sh /app/config/init_db.sh

ENTRYPOINT ["/app/config/init_db.sh"]
CMD ["bundle", "exec", "rails", "s", "-p", "3000", "-b", "0.0.0.0"]
