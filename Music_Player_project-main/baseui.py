
class BaseUI:
    def display_header(self, title):
        print(f"\n--- {title} ---")

    def get_valid_input(self, prompt, valid_options):
        choice = input(prompt)
        while choice not in valid_options:
            print("Invalid choice!")
            choice = input(prompt)
        return choice

    def paginate(self, items, page_size, page):
        start = (page - 1) * page_size
        end = start + page_size
        return items[start:end]
 
