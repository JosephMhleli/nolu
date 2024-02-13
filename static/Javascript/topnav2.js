function toggleNav() {
  var sidenav = document.getElementById("mySidenav");
  var icon = document.getElementById("menuIconSidenav");
  if (sidenav.style.width === "250px") {
    sidenav.style.width = "0";
    icon.classList.replace("fa-times", "fa-bars"); // Change icon to bars when the nav is closed
  } else {
    sidenav.style.width = "250px";
    icon.classList.replace("fa-bars", "fa-times"); // Change icon to times when the nav is open
  }
}


function closeNav() {
  var sidenav = document.getElementById("mySidenav");
  var overlay = document.getElementById("overlay");
  var menuIcon = document.getElementById("menuIcon");
  var closeIcon = document.getElementById("closeIcon");
  var menuIconSidenav = document.getElementById("menuIconSidenav");
  var sidenavItems = document.getElementById("sidenavItems");

  sidenav.style.width = "0";
  overlay.style.display = "none";
  menuIcon.style.display = "block";
  closeIcon.style.display = "none";
  menuIconSidenav.style.display = "block";
  sidenavItems.classList.add("hidden");
}
