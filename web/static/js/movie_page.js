// const ratingSubmit = document.querySelector(".ratingSubmit")
const ratingSection = document.querySelector(".rating")
// const numberOfRating = document.querySelector(" numberOfRating")
const movieDetail = document.querySelector(".movie__information")
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
const path = document.location['pathname'];

let userRating = document.querySelector("#rating").innerHTML;
if (userRating != ""){
    document.querySelector(`#star${userRating}`).checked=true
}

ratingSection.addEventListener("change",()=>{
    
    let ratingValue = document.querySelector('input[name="rating"]:checked').value
    let data = {"rating":ratingValue, "imdb_id":movieDetail.id}
    // numberOfRating.innerHTML = `Choose Rating :${ratingValue}`
    console.log(data)
    fetch("/rating",{
        method: "POST",
        mode: 'same-origin',
        
        body : JSON.stringify(data),
        headers : {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
    })

        .then((res)=>{

            return res.json()
        })
        .catch((error) => {
            window.location.href = `/signin?next=${path}`;
            console.log('Error:', error)
        })
        .then((json)=>{
            console.log(json)
        })
})
// ratingSubmit.addEventListener("click",()=>{
//     let ratingValue = document.querySelector('input[name="rating"]:checked').value
//     console.log(ratingValue)
// })







// offsetNum = 0
// main('/api/rating/?limit=12&offset=0',offsetNum)

// showMoreButton = document.querySelector(".showMore")
// showMoreButton.addEventListener("click",()=>{
//     offsetNum += 12
//     main(`/api/rating/?limit=12&offset=${offsetNum}`,offsetNum)
// })