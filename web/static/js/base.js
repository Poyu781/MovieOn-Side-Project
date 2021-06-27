
const searchButton = document.querySelector(".button__search")



searchButton.addEventListener("click",()=>{
    let search_value = document.querySelector("input[type='text']").value
    if (search_value){
        window.location.href = `/basicSearch?query=${search_value}`;
    }

})
document.addEventListener("keypress",(e)=>{
    if (e.key === 'Enter') {
        let search_value = document.querySelector("input[type='text']").value
        console.log(search_value)
        if (search_value){
            window.location.href = `/basicSearch?query=${search_value}`;
        }
    }
}
)
document.querySelector(".top__btn").addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  })
// searchButton.addEventListener("click",()=>{
//     let search_value = document.querySelector("input[type='text']").value
//     itemsSection.innerHTML = ""
//     showMoreButton.style.display = "none";
//     main(`/api/search?query=${search_value}`)
// })