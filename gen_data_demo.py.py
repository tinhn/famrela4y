import pandas as pd 
import csv
from collections import defaultdict

# ======================================================
person_info = {
    "Nguyễn Văn A":   {"gender": "Nam", "fam_order": 1},
    "Phạm Thị B":      {"gender": "Nữ", "fam_order": 1},
    "Nguyễn C":      {"gender": "Nam", "fam_order": 1},
    "Thị D":      {"gender": "Nữ", "fam_order": 2},
    ...   
}

family_data = [
    {"spouse": ["Nguyễn Văn A", "Trần Thị B"]},
    {"spouse": ["Lê Văn C"], "children": ["Nguyễn Văn A"]},
    {"spouse": ["Phạm Thị D"], "children": ["Trần Thị B"]},
    ...
]

def build_family_maps(families):
    spouse_map = {}
    couples = []
    children_map = defaultdict(list)
    parents_map = defaultdict(list)
    
    for fam in families:
        parents = fam.get("spouse")
        if len(parents) == 2:
            # lấy ra cặp vợ chồng
            couples.append(tuple(parents))
            
            # sinh ra cặp vợ/chồng - chồng/vợ hai chiều
            p1, p2 = parents            
            spouse_map[p1] = p2
            spouse_map[p2] = p1            

        # chỉ lấy ra những gia đình có con
        childrens = fam.get("children", [])        
        if parents and childrens:
            # map từng cha/mẹ với các con   
            for parent in parents:
                children_map[parent].extend(childrens)
            
            # map từng con với cha/mẹ 
            for child in childrens:
                parents_map[child].extend(parents)

    return spouse_map, couples, dict(children_map), dict(parents_map)

# spouse_map: Xác định cặp vợ - chồng 
# children_map: Xác định cha/mẹ - con
# parents_map: Xác định sui gia
# couples: Xác định sui gia
spouse_map, couples, children_map, parents_map = build_family_maps(families)


# ======================================================
# Hàm sinh cạnh sui gia
def generate_suigia_edges(parents_map, couples):
    sui_gia_pairs = set()

    for spouse1, spouse2 in couples:
        # Tìm cha mẹ của mỗi người (có thể rỗng hoặc chỉ có 1)
        parents1 = parents_map.get(spouse1, [])
        parents2 = parents_map.get(spouse2, [])

        # Nếu không có cha mẹ nào thì bỏ qua
        if not parents1 and not parents2:
            continue

        # Ghép từng cha mẹ bên này với từng cha mẹ bên kia
        for p1 in parents1:
            for p2 in parents2:
                if p1 != p2:
                    sui_gia_pairs.add(tuple(sorted([p1, p2])))

    # Sinh cạnh hai chiều
    edges = []
    for p1, p2 in sui_gia_pairs:
        edges.append((p1, "sui gia", p2))
        edges.append((p2, "sui gia", p1))
    return edges

# ======================================================
# Hàm sinh cạnh vợ chồng
def generate_spouse_edges(spouse_map):
    edges = []
    for person, spouse in spouse_map.items():
        label = "chồng" if person_info[person]["gender"] == "Nam" else "vợ"
        edges.append((person, label, spouse))
    return edges

# Hàm sinh cạnh cha mẹ - con
def generate_parent_child_edges(children_map):
    edges = []
    for parent, children in children_map.items():
        for child in children:
            # Chiều cha/mẹ → con
            gender = person_info.get(child, {}).get("gender")
            label_pc = "con trai" if gender == "Nam" else "con gái" if gender == "Nữ" else "con"
            edges.append((child, label_pc, parent))

            # Chiều con → cha/mẹ
            parent_gender = person_info.get(parent, {}).get("gender")
            label_cp = "cha ruột" if parent_gender == "Nam" else "mẹ ruột" if parent_gender == "Nữ" else "cha/mẹ ruột"
            edges.append((parent, label_cp, child))
    return edges

# Hàm suy luận con rể, cha vợ, mẹ vợ
def generate_inlaw_edges(spouse_map, children_map):
    edges = []
    for parent, children in children_map.items():
        for child in children:
            if child in spouse_map:
                spouse = spouse_map[child]
                
                if person_info[spouse]["gender"] == "Nam":
                    edges.append((spouse, "con rể", parent))
                    label = "cha vợ" if person_info[parent]["gender"] == "Nam" else "mẹ vợ"
                    edges.append((parent, label, spouse))
                if person_info[spouse]["gender"] == "Nữ":
                    edges.append((spouse, "con dâu", parent))
                    label = "cha chồng" if person_info[parent]["gender"] == "Nam" else "mẹ chồng"
                    edges.append((parent, label, spouse))
    return edges

# Hàm suy luận anh chị em
def generate_sibling_edges(children_map):
    # Hàm lấy ra nhãn
    def get_sibling_label(a, b):
        if person_info[a]["gender"] == "Nam" and person_info[b]["gender"] == "Nam":
            return "anh trai" if person_info[a]["fam_order"] < person_info[b]["fam_order"] else "em trai"
        elif person_info[a]["gender"] == "Nữ" and person_info[b]["gender"] == "Nữ":
            return "chị gái" if person_info[a]["fam_order"] < person_info[b]["fam_order"] else "em gái"
        elif person_info[a]["gender"] == "Nam" and person_info[b]["gender"] == "Nữ":
            return "em trai" if person_info[a]["fam_order"] > person_info[b]["fam_order"] else "anh trai"
        elif person_info[a]["gender"] == "Nữ" and person_info[b]["gender"] == "Nam":
            return "chị gái" if person_info[a]["fam_order"] < person_info[b]["fam_order"] else "em gái"
        else:
            return "anh chị em"
    
    edges = []
    sibling_groups = {}

    for parent, children in children_map.items():
        sibling_groups.setdefault(parent, set(children))

    seen = set()
    for siblings in sibling_groups.values():
        siblings = list(siblings)
        for i in range(len(siblings)):
            for j in range(len(siblings)):
                if i == j:
                    continue
                a, b = siblings[i], siblings[j]
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                seen.add((b, a))

                label_ab = get_sibling_label(a, b)
                label_ba = get_sibling_label(b, a)

                edges.append((a, label_ab, b))
                edges.append((b, label_ba, a))
    return edges

# Hàm suy luận quan hệ cháu nội / cháu ngoại
def generate_grandchild_edges(children_map):
    edges = []
    # Duyệt từng cặp cha mẹ → con
    for parent, children in children_map.items():
        for child in children:
            # Nếu đứa con này cũng là cha/mẹ của ai đó
            if child in children_map:
                grandchildren = children_map[child]
                for grandchild in grandchildren:
                    # Xác định giới tính của người trung gian (cha/mẹ)
                    gender = person_info.get(child, {}).get("gender")
                    if gender == "Nam":
                        # Cháu nội
                        edges.append((grandchild, "cháu nội", parent))
                        label = "ông nội" if person_info[parent]["gender"] == "Nam" else "bà nội"
                        edges.append((parent, label, grandchild))
                    elif gender == "Nữ":
                        # Cháu ngoại
                        edges.append((grandchild, "cháu ngoại", parent))
                        label = "ông ngoại" if person_info[parent]["gender"] == "Nam" else "bà ngoại"
                        edges.append((parent, label, grandchild))
    return edges


# Tổng hợp tất cả các cạnh
def generate_all_edges():
    edges = []
    
    edges += generate_spouse_edges(spouse_map)
    edges += generate_parent_child_edges(children_map)
    edges += generate_inlaw_edges(spouse_map, children_map)
    edges += generate_sibling_edges(children_map)
    edges += generate_grandchild_edges(children_map)
    edges += generate_suigia_edges(parents_map, couples)
    
    return edges


# Hiển thị kết quả ra màn hình 
def display_edges(edges):
    print("# Edges")
    print("Source, Label, Target")
    for source, label, target in edges:
        print(f"{source}, {label}, {target}")

# Hàm ghi file
def write_edges_to_csv(edges, filename="my-family-relation.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        # Ghi tiêu đề cột
        writer.writerow(["source", "label", "target"])
        # Ghi từng dòng dữ liệu
        for source, label, target in edges:
            writer.writerow([source, label, target])
    print(f"Đã ghi {len(edges)} cạnh vào file '{filename}'")


if __name__ == "__main__":
    # Gen ra cạnh
    edges = generate_all_edges()

    # Ghi ra file 
    write_edges_to_csv(edges)

    # # Hiển thị ra màn hình 
    # display_edges(sorted(edges))
