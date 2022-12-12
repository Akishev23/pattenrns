from views import Index, Contact, Page, Examples, AnotherPage

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/page/': Page(),
    '/examples/': Examples(),
    '/another_page/': AnotherPage(),
}
