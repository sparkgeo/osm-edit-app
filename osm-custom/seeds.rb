
Language.load(Rails.root.join("config/languages.yml"))

admin = User.find_or_initialize_by(:email => ENV["SUPERUSER_EMAIL"])
admin.update_attributes(
  :email => ENV["SUPERUSER_EMAIL"],
  :email_valid => true,
  :display_name => "SuperAdminUser",
  :description => "Super admin user for startup.",
  :status => "confirmed",
  :terms_seen => true,
  :terms_agreed => Time.now.getutc,
  :data_public => true,
  :pass_crypt => ENV["SUPERUSER_PWD"],
  :pass_crypt_confirmation => ENV["SUPERUSER_PWD"],
)
admin.roles.create(:role => "administrator", :granter_id => admin.id )


# OAuth Consumer Key for iD Editor
# Learn more at https://github.com/openstreetmap/openstreetmap-website/blob/master/CONFIGURE.md#oauth-consumer-keys

# application_params = {
#   :name => "iD_Local",
#   :url => ENV["OSM_URL"],
#   :allow_read_prefs => true,
#   :allow_write_api => true,
# }
# id = admin.client_applications.build(application_params)
# id.save


id = ClientApplication.find_or_initialize_by(:name => "iDGlobal")
id.update_attributes(
  :name => "iDGlobal",
  :url => ENV["OSM_URL"],
  :user_id => admin.id,
  :allow_read_prefs => true,
  :allow_write_api => true,
)
ClientApplication.all_permissions.each { |p| id[p] = true }
id.save

open('/app/config/settings.local.yml', 'a') do |f|
    f.puts "id_key: " + id.key
end
