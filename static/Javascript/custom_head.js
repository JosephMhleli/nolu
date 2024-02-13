class CustomHead extends HTMLElement {
    constructor() {
      super(); // Always call super first in constructor
      this.attachShadow({ mode: 'open' }); // Attach a shadow root to the element.
  
      // Define the content you want to reuse in the head section
      const content = `
      <script src="https://unpkg.com/feather-icons"></script>
      <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <script src="https://kit.fontawesome.com/324c7ccd76.js" crossorigin="anonymous"></script>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans&family=Roboto&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Diplomata+SC&family=Gorditas&family=Josefin+Sans:ital,wght@1,500&family=PT+Serif:ital@1&family=Vast+Shadow&family=Vollkorn&display=swap" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Ephesis&family=Josefin+Sans:ital,wght@0,100;1,100&display=swap" rel="stylesheet">
      `;
  
      // Append the content to the shadow DOM
      this.shadowRoot.innerHTML = content;
    }
  }
  
  // Define the new element
  customElements.define('custom-head', CustomHead);
  