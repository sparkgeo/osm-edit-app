FROM sparkgeo/osm-rails-port:v0.7

ADD ./land.html /app/public/land.html
ADD ./database.yml /app/config/database.yml
ADD ./storage.yml /app/config/storage.yml
ADD ./settings.local.yml /app/config/settings.local.yml

CMD ["bundle", "exec", "rails", "s", "-p", "3000", "-b", "0.0.0.0"]
