import bs4

from . import ALL_PAGES

def main():
  for page in ALL_PAGES:
    soup = bs4.BeautifulSoup((page.path / 'original.html').read_text(), 'html.parser')
    soup.find(id="holder")["contenteditable"] = "true"
    for paginator_index, button_text in [(0, 'Click me before making any edits, then paste into before-edit.html'), (-1, 'Click me after making your edits, then paste into after-edit.html')]:
      paginator: bs4.Tag = soup.find_all(class_='paginator')[paginator_index]
      copy_dom_button = soup.new_tag('button')
      copy_dom_button['id'] = f'copy_dom_button_{paginator_index}'
      copy_dom_button['onclick'] = '''
        (() => {
            var textArea = document.createElement("textarea");
            textArea.value = document.children[0].outerHTML;
            
            // Avoid scrolling to bottom
            textArea.style.top = "0";
            textArea.style.left = "0";
            textArea.style.position = "fixed";

            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
              var successful = document.execCommand('copy');
              var msg = successful ? 'successful' : 'unsuccessful';
              console.log('Fallback: Copying text command was ' + msg);
            } catch (err) {
              console.error('Fallback: Oops, unable to copy', err);
            }

            document.body.removeChild(textArea);

            document.getElementById("copy_dom_button_''' + str(paginator_index) + '''").innerText = "Copied!";
        })()
      '''
      copy_dom_button.append(soup.new_string(button_text))
      paginator.insert_before(copy_dom_button)
    (page.path / 'prep-edit.html').write_text(soup.prettify())

_DOIT_TASKSPEC = {
  'file_dep': [__file__, *(p.path / 'original.html' for p in ALL_PAGES)],
  'targets': [p.path / 'prep-edit.html' for p in ALL_PAGES],
  'actions': [main],
}
