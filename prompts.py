class Prompt:
    # The base class for all Prompts.
    # Has an internal type of 0 represented in the dictionary.

    def __init__(self, question):
        self.question = question
        self.type = 0

    def get_question(self):
        return self.question


class TextPrompt(Prompt):
    # The subclass for Text Prompts.
    # Has an internal type of 1.
    # Functionally identical to the base Prompt.

    def __init__(self, question):
        super().__init__(question)
        self.type = 1


class NumberPrompt(Prompt):
    # The subclass for Number Prompts.
    # Has an internal type of 2.
    # Supports bounding.

    def __init__(self, question):
        super().__init__(question)
        self.bounds = {"upper": None, "lower": None, "upper_inclusive": False, "lower_inclusive": False}

        self.type = 2

        # An inclusive upper bound means acceptable values are <= the bound. Otherwise, strictly <.
        # An inclusive lower bound means acceptable values are >= the bound. Otherwise, strictly >.

    def set_upper_bound(self, num):
        self.bounds["upper"] = num

    def set_lower_bound(self, num):
        self.bounds["lower"] = num

    def set_upper_bound_inclusive(self, val):
        self.bounds["upper_inclusive"] = val

    def set_lower_bound_inclusive(self, val):
        self.bounds["lower_inclusive"] = val

    def validate(self, user_input):
        # If upper_bound is set, fails if input is greater or equal.
        # If upper bound is inclusive, fails if input is exclusively greater.
        # If lower_bound is set, fails if input is lesser or equal.
        # If lower bound is inclusive, fails if input is exclusively lesser.
        user_num = int(user_input)

        if self.bounds["upper"]:
            if self.bounds["upper_inclusive"]:
                if user_num > self.bounds["upper"]:
                    return False
            else:
                if user_num >= self.bounds["upper"]:
                    return False

        if self.bounds["lower"]:
            if self.bounds["lower_inclusive"]:
                if user_num < self.bounds["lower"]:
                    return False
            else:
                if user_num <= self.bounds["lower"]:
                    return False

        return True


class MultiChoicePrompt(Prompt):
    # The subclass for Multiple Choice Prompts.
    # Has an internal type of 3.

    def __init__(self, question, options=None):
        super().__init__(question)
        self.options = []
        if options is not None:
            self.options = options
        self.type = 3

    def add_option(self, opt):
        self.options.append(opt)

    def remove_option(self, opt):
        self.options.remove(opt)

    def get_options(self):
        return self.options


class EmailPrompt(Prompt):
    # The subclass for Email Validation Prompts.
    # Has an internal type of 4.

    def __init__(self, question):
        super().__init__(question)
        self.domains = {"allowed": [], "blocked": []}
        self.type = 4

    def add_allowed_domain(self, domain):
        self.domains["allowed"].append(domain)

    def add_blocked_domain(self, domain):
        self.domains["blocked"].append(domain)

    def remove_allowed_domain(self, domain):
        self.domains["allowed"].remove(domain)

    def remove_blocked_domain(self, domain):
        self.domains["blocked"].remove(domain)

    def validate(self, user_input):
        # If there are no entries in the whitelist or blacklist, this function always returns true.
        # Otherwise, will return FALSE if the provided domain is in the blacklist or not in the whitelist.
        # Returns TRUE if the provided domain is in the whitelist or not in the blacklist.
        domain = user_input.split("@")[1]
        if self.domains["allowed"]:
            # We are doing whitelist validation FIRST.
            return domain in self.domains["allowed"]

        if self.domains["blocked"]:
            # We are doing blacklist validation SECOND.
            return domain not in self.domains["blocked"]

        return True


class PasswordPrompt(Prompt):
    # The subclass for Password Prompts.
    # Has an internal type of 5.

    def __init__(self, question):
        super().__init__(question)
        self.passwords = []
        self.type = 5

    def add_password(self, pw):
        self.passwords.append(pw)

    def remove_password(self, pw):
        self.passwords.remove(pw)

    def validate(self, user_input):
        return user_input in self.passwords


def prompt_from_dict(p_dict):
    prompt_type = p_dict["type"]
    if prompt_type == 1:
        # Text Prompt.
        prompt = TextPrompt(p_dict["question"])

    elif prompt_type == 2:
        # Number Prompt.
        prompt = NumberPrompt(p_dict["question"])
        bounds_check = p_dict["bounds"]

        prompt.set_lower_bound(bounds_check["lower"])
        prompt.set_upper_bound(bounds_check["upper"])
        prompt.set_lower_bound_inclusive(bounds_check["lower_inclusive"])
        prompt.set_upper_bound_inclusive(bounds_check["upper_inclusive"])

    elif prompt_type == 3:
        # Multiple Choice Prompt.
        prompt = MultiChoicePrompt(p_dict["question"])
        for opt in p_dict["options"]:
            prompt.add_option(opt)

    elif prompt_type == 4:
        # Email Validation Prompt.
        prompt = EmailPrompt(p_dict["question"])
        domain_block = p_dict["domains"]
        for dom in domain_block["allowed"]:
            prompt.add_allowed_domain(dom)
        for dom in domain_block["blocked"]:
            prompt.add_blocked_domain(dom)

    elif prompt_type == 5:
        # Password Prompt.
        prompt = PasswordPrompt(p_dict["question"])
        for pw in p_dict["passwords"]:
            prompt.add_password(pw)
    else:
        # Default blank prompt.
        prompt = Prompt(p_dict["question"])

    return prompt
