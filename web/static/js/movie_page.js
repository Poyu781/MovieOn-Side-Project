const itemsSection = document.querySelector(".itemsSection");
const ratingSubmit = document.querySelector(".ratingSubmit")
const ratingSection = document.querySelector(".rating")
const ratingNum = document.querySelector(".ratingNum")
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

console.log(csrftoken)
ratingSection.addEventListener("change",()=>{
    
    let ratingValue = document.querySelector('input[name="rating"]:checked').value
    let data = {"rating":ratingValue}
    ratingNum.innerHTML = `Choose Rating :${ratingValue}`
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
            console.error('Error:', error)
        })
        .then((json)=>{
            console.log(json)
        })
})
ratingSubmit.addEventListener("click",()=>{
    let ratingValue = document.querySelector('input[name="rating"]:checked').value
    console.log(ratingValue)
})






function renderMovies(movieObject, nodeDiv) {
    let node = document.createElement("div");
    node.classList.add("movie");
    node.setAttribute("id", movieObject.imdb.imdb_id)
    let img = movieObject.imdb.image;
    let title = movieObject.imdb.movie_title;
    let imdb_rating = movieObject.imdb_rating
    let rotten_audience_rating = movieObject.audience_rating
    let rotten_tomator_rating = movieObject.tomator_rating
    let douban_rating = movieObject.douban_rating
    let htmlText = `
  <img src=${img}>
  <div class="information">
    <div class="productInfo">
      <div>${title}</div>
      <div>IMDb:${imdb_rating}</div>
      <div>Rotten Audience:${rotten_audience_rating}</div>
      <div>Rotten Reviewer:${rotten_tomator_rating}</div>
      <div>Douban :${douban_rating}</div>
    </div>
  </div>
  `;
    node.innerHTML = htmlText;
    nodeDiv.appendChild(node);
}


function main(url,offsetNum) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {

            let dataArray = datalist["results"]; //I will get a list of dict
            console.log(dataArray)
            let num = dataArray.length;
// Math.ceil(offsetNum/4);
            if (offsetNum == 0){
                let node = document.createElement("div");
                node.classList.add("itemsWrap");
                // node.setAttribute("id", `wrap${row}`);
                itemsSection.appendChild(node);
            }
            itemsWrap = document.querySelector('.itemsWrap');
            for (let i = 0; i < num; i++) {

                try {
                    renderMovies(dataArray[i], itemsWrap);
                } catch {
                    let node = document.createElement("div");
                    node.classList.add("item");
                    itemsWrap.appendChild(node);
                }
            }

        });
}
// offsetNum = 0
// main('/api/rating/?limit=12&offset=0',offsetNum)

// showMoreButton = document.querySelector(".showMore")
// showMoreButton.addEventListener("click",()=>{
//     offsetNum += 12
//     main(`/api/rating/?limit=12&offset=${offsetNum}`,offsetNum)
// })