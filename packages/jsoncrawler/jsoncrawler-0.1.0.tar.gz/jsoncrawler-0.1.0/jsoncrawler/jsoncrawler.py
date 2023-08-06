from collections import deque


class JsonCrawler:
    """
    Helps you retrieve select specific values from large JSONs without writing verbose for-loops.
    """

    @staticmethod
    def get_first(raw_json, search_key):
        """
        Gets value for only the first encounter with this key during its search.
        Returns [] by default if no key found.

        'search_key' must be the value of the key to search for.
        Please ensure 'search_key' has an immutable value.

        EXAMPLE

        json = {
            "example1": "value1_1",
            "example3": {
                "example1": "value1_2",
                "example2": "value2_2",
            },
            "example2": "value2_1",
        }

        JsonCrawler.get_first(raw_json, "example1")
        :return [value1_1]

        JsonCrawler.get_first(raw_json, "example2")
        :return [value2_1]

        JsonCrawler.get_first(raw_json, "example5")
        : return []

        """

        # Pre-test: Type check
        JsonCrawler._verify_json(raw_json)

        check_elements = deque([raw_json])

        while check_elements:
            lst_or_dict = check_elements.pop()

            if isinstance(lst_or_dict, dict):
                for key, value in lst_or_dict.items():

                    if key == search_key:
                        return [value]

                    elif isinstance(value, list):
                        check_elements.extend(value)

                    elif isinstance(value, dict):
                        check_elements.append(value)

            elif isinstance(lst_or_dict, list):
                JsonCrawler._unpack_list(lst_or_dict, check_elements)

        return []

    @staticmethod
    def get_all(raw_json, search_key):
        """
        Gets all values that match the provided key
        Returns [] by default if no key found.

        'search_key' must be the value of the key to search for.
        Please ensure 'search_key' has an immutable value.

        EXAMPLE

        json = {
            "example1": "value1_1",
            "example3": {
                "example1": "value1_2",
                "example2": "value2_2",
            },
            "example2": "value2_1"

        }

        JsonCrawler.get_all(raw_json, "example1")
        :return ["value1_1", "value1_2"]

        JsonCrawler.get_all(raw_json, "example2")
        :return ["value2_1", "value2_2"]

        JsonCrawler.get_all(raw_json, "example3")
        :return [{"example1": "value1_2", "example2": "value2_2"}]

        JsonCrawler.get_all(raw_json, "example5")
        :return []

        """

        # Pre-test: Type check
        JsonCrawler._verify_json(raw_json)

        return JsonCrawler._get_values(raw_json, search_key)

    @staticmethod
    def get_many_keys(raw_json, search_keys=set()):
        """
        Gets all values for all provided keys.
        'search_keys' must be a set containing keys to search for.
        Please ensure each key in 'search_keys' is immutable.
        Returns [] by default if no keys found.

        EXAMPLE

        json = {
            "example1": "value1_1",
            "example3": {
                "example1": "value1_2",
                "example2": "value2_2",
            },
            "example2": "value2_1"

        }

        JsonCrawler.get_many_keys(raw_json, {"example1", "example2"})
        :return ['value1_1', 'value2_1', 'value1_2', 'value2_2']

        JsonCrawler.get_many_keys(raw_json, {"example5})
        :return []

        """

        # Pre-test: Type check
        JsonCrawler._verify_json(raw_json)

        # Pre-test: Type check
        if not isinstance(search_keys, set):
            error_msg = (
                f"TypeError: Expected Set for 'search_keys'. Received: {type(raw_json)}. "
            )
            raise AssertionError(error_msg)

        # Pre-test: No search keys passed
        if len(search_keys) == 0:
            error_msg = "ValueError: Expected non-empty set for 'search_keys'. Received: empty set."
            raise AssertionError(error_msg)

        extracted_values = []
        check_elements = deque([raw_json])

        while check_elements:
            lst_or_dict = check_elements.pop()

            if isinstance(lst_or_dict, dict):
                for key, value in lst_or_dict.items():

                    if key in search_keys:
                        extracted_values.append(value)

                    if isinstance(value, list):
                        check_elements.extend(value)

                    elif isinstance(value, dict):
                        check_elements.append(value)

            elif isinstance(lst_or_dict, list):
                JsonCrawler._unpack_list(lst_or_dict, check_elements)

        return extracted_values

    @staticmethod
    def get_descendants(raw_json, search_keys):
        """
        Searches through keys and returns descendant values.
        Keys that come later are assumed to be descendants of earlier keys.
        'search_keys' must be a list of keys to search for.
        Please ensure each key in 'search_keys' is immutable.
        Returns [] if any of the parent keys are not found.

        Has the ability to crawl the entire JSON regardless of depth.
        Automatically crawls nested lists and nested dictionaries.

        In case search_keys is a list of only 1 key
        => JsonCrawler.get_descendants(["key"]) == JsonCrawler.get_all("key")

        EXAMPLE

        search_keys = ["default", "images", "zoom"]
        Above returns all values of "zoom" key,
        which has "images" as a parent,
        which has "default" as a parent.

        EXAMPLE

        json = {
            "example1": "value1_1",
            "example3": {
                "example1": "value1_2",
                "example2": "value2_2",
                "example5": [
                    {
                        "example4": "value4_1"
                    }
                ],
                "example6": {
                    "example4": "value4_2",
                },
            },
            "example2": {
                "example4": "value4_3",
            }

        }

        JsonCrawler.get_descendants(raw_json, ["example4"])
        Interpretation --> get all values of the "example4" key.
        :return ["value4_1", "value4_2", "value4_3"]

        JsonCrawler.get_descendants(raw_json, ["example3", "example4"])
        Interpretation --> get all values of "example4" ONLY when it is a descendant of "example3".
        :return ["value4_1", "value4_2"]

        JsonCrawler.get_descendants(raw_json, ["example5", "example4"])
        Interpretation --> get all values of "example4" ONLY when it is a descendant of "example5".
        :return ["value4_1"]

        JsonCrawler.get_descendants(raw_json, ["example2", "example4" ])
        Interpretation --> get all values of "example4" ONLY when it is a descendant of "example2".
        :return ["value4_3"]

        JsonCrawler.get_descendants(raw_json, ["example1", "example4"])
        Interpretation --> get all values of "example4" ONLY when it is a descendant of "example1".
        :return []

        """

        # Pre-test: Type check
        JsonCrawler._verify_json(raw_json)

        # Pre-test: Type check
        if not isinstance(search_keys, list):
            error_msg = (
                f"TypeError: Expected List for 'search_keys'. Received: {type(search_keys)}."
            )
            raise AssertionError(error_msg)

        # Pre-test: No search keys passed
        if len(search_keys) == 0:
            error_msg = (
                "ValueError: Expected a non-empty list for 'search_keys'. Received: empty list."
            )
            raise AssertionError(error_msg)

        search_keys = deque(search_keys)
        search_key = search_keys.popleft()
        extracted_values = JsonCrawler._get_values(raw_json, search_key)

        while search_keys:
            search_key = search_keys.popleft()

            if extracted_values:
                extracted_values = JsonCrawler._get_values(extracted_values, search_key)

        return extracted_values

    @staticmethod
    def _get_values(lst_or_dict, search_key=None):
        """
        This function iterates through a JSON and retrieves all values that match a key.
        This is a private method to be used in the JsonCrawler class.
        Since it is a private method, no tests have been written for it.

        lst_or_dict: will accept any JSON or list of JSONs.
        search_key: the key you want to match.
        return: a list containing all values that had a key matching 'search_key'.

        Example: JsonCrawler._get_values(raw_json, "url")
        """

        extracted_values = []
        check_elements = deque([lst_or_dict])

        while check_elements:
            lst_or_dict = check_elements.pop()

            if isinstance(lst_or_dict, dict):
                for key, value in lst_or_dict.items():

                    if key == search_key:
                        extracted_values.append(value)

                    if isinstance(value, list):
                        check_elements.extend(value)

                    elif isinstance(value, dict):
                        check_elements.append(value)

            elif isinstance(lst_or_dict, list):
                JsonCrawler._unpack_list(lst_or_dict, check_elements)

        return extracted_values

    @staticmethod
    def _unpack_list(lst, check_elements):
        for element in lst:
            if isinstance(element, list):
                check_elements.extend(element)

            elif isinstance(element, dict):
                check_elements.append(element)

    @staticmethod
    def _verify_json(raw_json):
        if not (isinstance(raw_json, list) or isinstance(raw_json, dict)):
            error_msg = f"TypeError: Expected List or Dictionary for 'raw_json'. Received: {type(raw_json)}."
            raise AssertionError(error_msg)
