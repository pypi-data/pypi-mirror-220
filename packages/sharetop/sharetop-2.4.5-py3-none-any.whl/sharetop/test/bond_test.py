from sharetop.core.bond.get_bond_public_info import bond_treasure_issue_cninfo, bond_local_government_issue_cninfo
from sharetop.core.bond.get_bond_info import get_bond_public, get_bond_base_info, get_bond_base_info_list

token = "f109298d079b5f60"


# d = bond_treasure_issue_cninfo()

# d = bond_local_government_issue_cninfo()

d = get_bond_base_info(token, "113672")

# d = get_bond_base_info_list(token)

print(d)