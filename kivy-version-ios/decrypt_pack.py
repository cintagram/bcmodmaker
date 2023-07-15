import helper
import os
from Cryptodome.Cipher import AES
from alive_progress import alive_bar 

output_path = "game_files"
lists_paths = "decrypted_lists"

def unpack_list(ls_file):
    data = helper.open_file_b(ls_file)
    key = helper.md5_str("pack")
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(data)
    return decrypted_data

def decrypt_pack(chunk_data, jp, pk_name, country_code):
    aes_mode = AES.MODE_CBC
    if jp:
        key = bytes.fromhex("d754868de89d717fa9e7b06da45ae9e3")
        iv = bytes.fromhex("40b2131a9f388ad4e5002a98118f6128")
    elif country_code == "en":
        key = bytes.fromhex("0ad39e4aeaf55aa717feb1825edef521")
        iv = bytes.fromhex("d1d7e708091941d90cdf8aa5f30bb0c2")

    elif country_code == "kr":
        key = bytes.fromhex("bea585eb993216ef4dcb88b625c3df98")
        iv = bytes.fromhex("9b13c2121d39f1353a125fed98696649")
    
    if "server" in pk_name.lower():
        key = helper.md5_str("battlecats")
        iv = None
        aes_mode = AES.MODE_ECB
    if iv:
        cipher = AES.new(key, aes_mode, iv)
    else:
        cipher = AES.new(key, aes_mode)
    decrypted_data = cipher.decrypt(chunk_data)
    return decrypted_data


def unpack_pack(pk_file_path, ls_data, jp, base_path, country_code):
    list_data = ls_data.decode("utf-8")
    split_data = helper.parse_csv_file(None, list_data.split("\n"), 3)

    pack_data = helper.open_file_b(pk_file_path)

    
    for i in range(len(split_data)):
        file = split_data[i]
        
        name = file[0]
        start_offset = int(file[1])
        length = int(file[2])

        pk_chunk = pack_data[start_offset:start_offset+length]
        base_name = os.path.basename(pk_file_path)
        if "imagedatalocal" in base_name.lower():
            pk_chunk_decrypted = pk_chunk
        else:
            pk_chunk_decrypted = decrypt_pack(pk_chunk, jp, base_name, country_code)
        helper.write_file_b(os.path.join(base_path, name), pk_chunk_decrypted)
            

def decrypt(jp, country_code):
    
    
    pack_paths = helper.select_files("PACK 파일을 선택해주세요.", [(".pack files", "*.pack")], False)
    if not pack_paths:
        return
    else:
        helper.check_and_create_dir(output_path)
    
    file_groups = find_lists(pack_paths)


    for i in range(len(file_groups)):
        file_group = file_groups[i]

        ls_base_name = os.path.basename(file_group["list"])
        pk_base_name = os.path.basename(file_group["pack"])

        name = pk_base_name.rstrip(".pack")
        path = os.path.join(output_path, name)

        helper.check_and_create_dir(path)
        helper.check_and_create_dir(lists_paths)

        ls_data = unpack_list(file_group["list"])
        helper.write_file_b(os.path.join(lists_paths, ls_base_name), ls_data)

        helper.coloured_text(f"\n&{i+1}&\t\t{name}\t{i+1} / {len(file_groups)}", base=helper.green, new=helper.white)
        unpack_pack(file_group["pack"], ls_data, jp, path, country_code)
    #helper.coloured_text(f"\nSuccessfully decrypted all .pack files to: &{output_path}&", base=helper.green, new=helper.white)
def find_lists(pack_paths):
    files = []
    for pack_path in pack_paths:
        directory = os.path.dirname(pack_path)
        ls_path = os.path.join(directory, pack_path.rstrip(".pack") + ".list")
        group = {"pack" : pack_path, "list" : ls_path}
        files.append(group)
    return files
