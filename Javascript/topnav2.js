function showCategory(category) {
    var content = '';

    switch (category) {
      case 1:
        // Check if the category is ROMANCE
        if (category === 1) {
          content = '<h2>Category 1</h2><div class="tobchosen"><p>Lihle</p></div>';
        } else {
          content = '<h2>Category 1</h2><div class="tobchosen"><a href="#ews">ROMANCE</a><a href="#ews">CHILDREN</a><a href="#ews">FICTION</a><a href="#ews">NON-FICTION</a></div>';
        }
        break;
      case 2:
        content = '<h2>Category 2</h2><div class="tobchosen"><a href="#ews">ROMANCE</a><a href="#ews">CHILDREN</a><a href="#ews">FICTION</a><a href="#ews">NON-FICTION</a></div>';
        break;
      case 3:
        content = '<h2>Category 3</h2><div class="tobchosen"><a href="#ews">ROMANCE</a><a href="#ews">CHILDREN</a><a href="#ews">FICTION</a><a href="#ews">NON-FICTION</a></div>';
        break;
      // Add more cases as needed

      default:
        content = '';
    }

    document.getElementById('hoverContent').innerHTML = content;
    document.querySelector('.hoverdiv').style.display = 'block';
  }

  function hideHoverDiv() {
    document.querySelector('.hoverdiv').style.display = 'none';
  }