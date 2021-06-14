
const searchButton = document.querySelector(".button__search")



searchButton.addEventListener("click",()=>{
    let search_value = document.querySelector("input[type='text']").value
    if (search_value){
        window.location.href = `/basicSearch?query=${search_value}`;
    }
    // 
    // main(`/api/search?query=${search_value}`)
})
// searchButton.addEventListener("click",()=>{
//     let search_value = document.querySelector("input[type='text']").value
//     itemsSection.innerHTML = ""
//     showMoreButton.style.display = "none";
//     main(`/api/search?query=${search_value}`)
// })