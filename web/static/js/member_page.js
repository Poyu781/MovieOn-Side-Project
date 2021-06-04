// const ratingSubmit = document.querySelector(".ratingSubmit")

// const numberOfRating = document.querySelector(" numberOfRating")
const reviewedSection= document.querySelector(".movies__block")

const userId = document.querySelector(".user").id
console.log(userId)


function renderMovies(movieObject, nodeDiv) {
    let node = document.createElement("div");
    node.classList.add("movie__information");
    node.setAttribute("id", movieObject.internal_id)
    
    let img = movieObject.img;
    let internal_rating = movieObject.rating
    let internal_id = movieObject.internal
    let title_name = movieObject.main_taiwan_name

    let htmlText = `
    <a class="movie-ranking" href="movie/${internal_id}">
  <img src=${img} />
  <div class="movie__info">
    <h4>${title_name}</h4>
    <h5>${internal_rating}<span>分</span></h5>
  </div>
  </a>
`;
    node.innerHTML = htmlText;
    nodeDiv.appendChild(node);
}


function main(url,node) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {
            let dataArray = datalist; //I will get a list of dict
            let num = dataArray.length;
// Math.ceil(offsetNum/4);
            for (let i = 0; i < num; i++) {
                renderMovies(dataArray[i], node);
            }

        });
    }
main(`api/member/${userId}/movies/`,reviewedSection)
const similartiySection = document.querySelector(".similarity")
function get_similarity(url,nodeDiv){
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {

            let dataArray = datalist[0]
            let imdb_sim = Math.round(dataArray.imdb*100,2);
            let douban_sim = Math.round(dataArray.douban*100,2)
            let tomato_sim = Math.round(dataArray.tomato*100,2)

            let htmlText = `
            <div class="similarity__block">
            <p>與 Imdb 相似程度</p>
            <div class="progress" data-percent="${imdb_sim}%" style="--percent: ${imdb_sim}px; --background: #f3ce13"></div>
          </div>
          <div class="similarity__block">
            <p>與 豆瓣 相似程度</p>
            <div class="progress" data-percent="${douban_sim}%" style="--percent: ${douban_sim}px; --background: #08CE14"></div>
          </div>
          <div class="similarity__block">
            <p>與 爛番茄觀眾 相似程度</p>
            <div class="progress" data-percent="${tomato_sim}%" style="--percent: ${tomato_sim}px; --background: #F70006"></div>
          </div>
        `;
        nodeDiv.innerHTML = htmlText;

})}
get_similarity(`api/member/${userId}/similarity/`,similartiySection)

function renderView(movieObject, nodeDiv) {
    
    let img = movieObject.img;
    let internal_id = movieObject.internal
    let title_name = movieObject.main_taiwan_name

    let htmlText = `
    <a class="movie-card" href="movie/${internal_id}">
    <img src=${img} />
    <div class="movie__info">
      <h4>${title_name}</h4>
    </div>
     
    </a>
`;
    nodeDiv.innerHTML = htmlText ;
}
viewedSection = document.querySelector(".xo")
function get_viewed(url,nodeDiv){
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {
            let num = datalist.length;
            console.log(3)
            for (let i = 0; i < num; i++) {
                renderView(datalist[i], viewedSection);
            }
            // let htmlText = 
        // nodeDiv.innerHTML = htmlText;

})}
get_viewed(`api/member/${userId}/viewed_movie/`,"de")
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
// const path = document.location['pathname'];

// let userRating = document.querySelector("#rating").innerHTML;

// if (userRating != ""){
//     console.log(userRating)
//     document.querySelector(`#star${userRating}`).checked=true
// }
// const ratingSection = document.querySelector(".rating")
// ratingSection.addEventListener("change",(e)=>{
//     let ratingValue = document.querySelector('input[name="rating"]:checked').value
//     let data = {"rating":ratingValue, "imdb_id":internalId}
//     // numberOfRating.innerHTML = `Choose Rating :${ratingValue}`
//     console.log(data)
//     fetch("/rating",{
//         method: "POST",
//         mode: 'same-origin',
        
//         body : JSON.stringify(data),
//         headers : {
//             'X-Requested-With': 'XMLHttpRequest',
//             'X-CSRFToken': csrftoken,
//             'Content-Type': 'application/json'
//         },
//     })

//         .then((res)=>{

//             return res.json()
//         })
//         .catch((error) => {
//             window.location.href = `/signin?next=${path}`;
//             console.log('Error:', error)
//         })
//         .then((json)=>{
//             console.log(json)
//         })
//     })