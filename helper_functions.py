class HelperFunctions():
    """ Helper functions used in ArtAnnounce Project"""

    def create_caption(self, firstname, lastname, title, height, length, 
        medium, substrate, website, genre):
        """create a caption out of ArtWork object"""

        caption = "#art"

        if genre:
            caption = ("#%s " % genre) + caption
        if website:
            caption = website + " " + caption
        if (medium and substrate):
            caption = ("%s on %s " % (medium, substrate)) + caption
        if (height and length):
            caption = ("%sx%s " % (height, length)) + caption
        if (title):
            caption = ("'%s' " % title) + caption
        if (firstname and lastname):
            caption = ("%s %s " % (firstname, lastname)) + caption

        return caption

    def test_create_caption(self):

        caption1 = create_caption(firstname='Kushlani', lastname='Jayasinha', title="Adventures to Beethoven's sixth (pastoral)", 
            height='30"', length='30"', medium='oil', substrate='canvas', 
            website="http://KushlaniFineArt.com", genre='abstracts')
        assertEqual(caption1, "Kushlani Jayasinha 'Adventures to Beethoven's sixth (pastoral)'")

        caption2 = create_caption(firstname='Kushlani', lastname='Jayasinha')
        assertEqual(caption2, "Kushlani Jayasinha")

        caption3 = create_caption(medium='oil', substrate='canvas', height='30"', length='30"',
            website="http://KushlaniFineArt.com", genre='abstracts')
        assertEqual(caption3, '30"x30" oil on canvas http://KushlaniFineArt.com  #abstracts #art')


if __name__ == "__main__":

    helper = HelperFunctions()

    helper.test_create_caption()


