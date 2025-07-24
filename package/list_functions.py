def show_list(list_given):
    for record in list_given:
        for key, value in record.items():
            print(f"{key}: {value}", end=" ", flush= True)
        print("")