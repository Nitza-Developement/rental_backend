from html.parser import HTMLParser


def get_fieldtype(attrs):
    """Return the field type of the tag"""
    for key, value in attrs:
        if key == "field-type":
            return value
    return None


class CustomHTMLParser(HTMLParser):
    template = ""
    fields = []
    add = True

    def handle_starttag(self, tag, attrs):
        self.add = True

        field_type = get_fieldtype(attrs)

        if field_type:

            field = self.get_field()

            if field_type == "SIGNATURE":
                self.template += f"<{tag}>"
            else:
                self.template += f"<{tag} class='content'>"

            content = field.get("response").get("content")
            image = field.get("response").get("url_file")

            if field_type == "EMAIL":
                self.template += f'<a href="mailto:{content}">{content}</a>'

            elif field_type == "PHONE":
                self.template += f'<a href="tel:{content}">{content}</a>'

            elif field_type == "SIGNATURE" and image:
                self.template += f'<img class="image" src="{image}" alt="Signature">'

            else:
                self.template += content

            self.add = False

        else:
            self.template += f"<{tag}>"

    def handle_endtag(self, tag):
        self.template += f"</{tag}>"

    def handle_data(self, data: str):
        if self.add:
            self.template += data

    def feed(self, data: str, fields):  # pylint: disable=arguments-differ
        self.fields = fields
        return super().feed(data)

    def get_field(self):
        """Return the current field"""
        field = self.fields[0]
        self.fields = self.fields[1:]
        return field
