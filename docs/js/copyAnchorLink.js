const links = document.querySelectorAll('h2[id], h3[id], h4[id], h5[id], h6[id], a[id]');
links.forEach(link => {
    link.addEventListener('click', event => {
        // Copy the anchor link to the clipboard
        navigator.clipboard.writeText(window.location.href + '#' + link.id);
        // console.log('Copied anchor link to clipboard: ' + window.location.href + '#' + link.id);
        // TODO: Show a toast message to the user
    }
)});