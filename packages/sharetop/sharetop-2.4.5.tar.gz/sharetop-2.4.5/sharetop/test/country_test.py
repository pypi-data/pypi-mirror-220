from sharetop.core.country.country_base_info import get_country_base_info

token = "f109298d079b5f60"


d = get_country_base_info(token)

print(d.to_dict("records"))