document.addEventListener("DOMContentLoaded", function() {

 const logolink = document.querySelectorAll(".menu-link");
 const primary_btn = document.querySelectorAll(".primary-btn");
const log_sig = document.querySelectorAll(".log_sig");

  logolink.forEach(logolink => {
    logolink.addEventListener("mouseover", () => {
      logolink.style.backgroundColor = "#39106b";
      
      
    });
  });
 logolink.forEach(logolink => {
    logolink.addEventListener("mouseout", () => {
      logolink.style.backgroundColor = null;
      logolink.style.margin = null;
    });
  });


primary_btn.forEach(primary_btn => {
    primary_btn.addEventListener("mouseover", () => {
      primary_btn.style.backgroundColor = "blue";
      
      
    });
  });
 primary_btn.forEach(primary_btn => {
    primary_btn.addEventListener("mouseout", () => {
      primary_btn.style.backgroundColor = null;
      
    });
  });


  log_sig.forEach(log_sig => {
    log_sig.addEventListener("mouseover", () => {
      log_sig.style.color = "purple";
      
    });
  });
  log_sig.forEach(log_sig => {
    log_sig.addEventListener("mouseout", () => {
      log_sig.style.color = null;
      
    });
  });

});
    

