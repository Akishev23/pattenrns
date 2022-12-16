from views import Index, Contact, Page, Examples, AnotherPage, Css

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/page/': Page(),
    '/examples/': Examples(),
    '/another_page/': AnotherPage(),
    '/style/': Css()
}
