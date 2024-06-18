def save_user_text(self):
        
        try:
            with open('user_text.json', 'r') as file:
                data = json.load(file)
            if not isinstance(data, dict) or "user_texts" not in data:
                data = {"user_texts": []}
        except FileNotFoundError:
            data = {"user_texts": []}

       
        data["user_texts"].append(self.user_text.strip())

        
        with open('user_text.json', 'w') as file:
            json.dump(data, file, indent=4)