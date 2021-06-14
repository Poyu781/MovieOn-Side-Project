// const ratingSubmit = document.querySelector(".ratingSubmit")
// const numberOfRating = document.querySelector(" numberOfRating")
const movieDetail = document.querySelector(".movie__information")
const movieSection= document.querySelector(".movie__section")
const movieNode = document.querySelector(".movie__all")
const movieRecommend = document.querySelector(".movie__recommend")
const featureObject = {'Comedy': 1, 'Fantasy': 2, 'Romance': 3, 'Drama': 4, 'Action': 5, 'Thriller': 6, 'War': 7, 'Adventure': 8, 'Animation': 9, 'Family': 10, 'Mystery': 11, 'Horror': 12, 'Sci-Fi': 13, 'Crime': 14, 'Biography': 15, 'History': 16, 'Music': 17, 'Sport': 18, 'Western': 19, 'Musical': 20, 'Documentary': 21, 'Adult': 22, 'News': 24}
let str = window.location.pathname;
let internalId = str.match(/[0-9].*/)[0];
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
function numberWithCommas(x) {
	try{
		return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	}
	catch{
		return x
	}
}
function renderMovies(movieObject, nodeDiv) {
    let node = document.createElement("section");
    node.classList.add("movie__section");
    
    let img = movieObject.img;
    let cnTitle = movieObject.main_taiwan_name;
    let engTitle = movieObject.main_original_name;
    let theaterDate = movieObject.date_in_theater
    let runTime = movieObject.runtime_minutes
    let imdbId = movieObject.imdb_id
    let doubanId = movieObject.douban_id
    let tomatoId = movieObject.rotten_tomato_id
    let imdbRating = movieObject.rating
    let imdbCount = numberWithCommas(movieObject.rating_count)
    let rottenAudienceRating = movieObject.audience_rating
    let rottenAudienceCount = numberWithCommas(movieObject.audience_rating_amount)
    let rottenTomatorRating = movieObject.tomator_rating
    let rottenTomatorCount = numberWithCommas(movieObject.tomator_rating_amount)
    let doubanRating = movieObject.avg_rating
    let doubanRatingCount = numberWithCommas(movieObject.total_rating_amount)
    let director_list = movieObject.director_list
    let actor_list = movieObject.actor_list
    let feature_list = movieObject.feature_list
	let htmlText = `
	<h2>${cnTitle} ${engTitle}</h2>
	<div class="movie__information" id=${movieObject.internal_id}>
	   <div class="movie__information-left">
		 <i class="fa fa-heart" id="heart" ></i>
		 <img src=${img} >
		 <div class="rating__wrap">
		  <div class="rating">你的評價： 7分<p></p>
		  <input type="radio" id="star10" name="rating" value="10"><label for="star10" title="Rocks!">10 stars</label>
		  <input type="radio" id="star9" name="rating" value="9"><label for="star9" title="Rocks!">9 stars</label>
		  <input type="radio" id="star8" name="rating" value="8"><label for="star8" title="Pretty good">8 stars</label>
		  <input type="radio" id="star7" name="rating" value="7"><label for="star7" title="Pretty good">7 stars</label>
		  <input type="radio" id="star6" name="rating" value="6"><label for="star6" title="Meh">6 star</label>
		  <input type="radio" id="star5" name="rating" value="5"><label for="star5" title="Meh">5 stars</label>
		  <input type="radio" id="star4" name="rating" value="4"><label for="star4" title="Kinda bad">4 stars</label>
		  <input type="radio" id="star3" name="rating" value="3"><label for="star3" title="Kinda bad">3 stars</label>
		  <input type="radio" id="star2" name="rating" value="2"><label for="star2" title="Sucks big time">2 stars</label>
		  <input type="radio" id="star1" name="rating" value="1"><label for="star1" title="Sucks big time">1 star</label>
		</div>
	  </div>
		 </div>
	  <div class="movie__detail">
		<ul>
		  <li>導演：${director_list}
  </li>
		  <li >演員：<br>${actor_list}</li>
		  <li>片長：${runTime} 分鐘</li>
		  <li>上映日期：${theaterDate}</li>
		  <li>類型：${feature_list}</li>
		</ul>
  <div class="movie__ranking">
		<a href="https://www.imdb.com/title/${imdbId}" target="_blank">
		  <div class="ranking__icon__wrapper">
		  <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/imdb.png">
			</div>
		  <p class="score">${imdbRating}</p>
		  <p>（共 ${imdbCount} 筆評分）</p>
		</a>
		<a href="https://movie.douban.com/subject/${doubanId}" target="_blank">
		<div class="ranking__icon__wrapper">
		  <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/douban.jpg">
		</div>
		  <p class="score">${doubanRating}</p>
		  <p>（共 ${doubanRatingCount}  筆評分）</p>
		</a>
		<a href="https://www.rottentomatoes.com/m/${tomatoId}" target="_blank">
		  <div class="ranking__icon__wrapper">
		  <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/tomato.png">
		  </div>
			<p class="score">${rottenAudienceRating}</p>
			<p>觀眾評分（共 ${rottenAudienceCount} 筆評分）</p>
		 </a>
		  <a href="https://www.rottentomatoes.com/m/${tomatoId}" target="_blank">
		  <div class="ranking__icon__wrapper">
		  <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/tomato.png">
		  </div>
		  <p class="score">${rottenTomatorRating}</p>
		  <p>影評評分（共 ${rottenTomatorCount} 筆評分）</p>
		 </a>
		 </div>
  </div></div>
	`
    descriptionNode = document.createElement("div")
    descriptionNode.classList.add("movie__intro");
    descriptionNode.innerHTML =`<h3>電影敘述</h3>${movieObject.chinese_description}`
    node.innerHTML = htmlText;
    nodeDiv.appendChild(node);
	nodeDiv.appendChild(descriptionNode);
	
}
function ratingFun(){
	let userRating = document.querySelector("#rating").innerHTML;

	if (userRating != ""){
		console.log(userRating)
		document.querySelector(`#star${userRating}`).checked=true
	}
	const ratingSection = document.querySelector(".rating")
	ratingSection.addEventListener("change",(e)=>{
		let ratingValue = document.querySelector('input[name="rating"]:checked').value
		let data = {"rating":ratingValue, "imdb_id":internalId}
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
}
function heartButton() {
	let heart = document.querySelector('#heart');
	heart.addEventListener('click', function() {
	  	heart.classList.toggle('red');
	});
  }
  
function renderRecommend(url,node){
	fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {
			let dataArray = datalist; //I will get a list of dict
			dataNum = dataArray.length
			console.log(dataArray)
			let nums = [], numsLen = 10, maxNum = Math.min(dataNum,25), num; 
			while (nums.length < numsLen) { 
				num = Math.round(Math.random() * maxNum); 
				if (nums.indexOf(num) === -1) { 
				 nums.push(num); 
				} 
			} 
			for (let i of nums){
				let internalId = dataArray[i].internal
				nodeCreated = document.createElement("a")
				nodeCreated.classList.add("movie");
				nodeCreated.setAttribute('href', `/movie/${internalId}`)
				nodeCreated.innerHTML= `
				<img src=${dataArray[i].img}>
			<div class="movie__info">
			<h3>${dataArray[i].main_taiwan_name}</h3>
			<div class="rank">
				<div>
				<img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/imdb.png">
				<p>${dataArray[i].imdb_rating}</p>
				</div>
				<div>
				<img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/douban.jpg">
				<p>${dataArray[i].douban_rating}</p>
				</div>
				<div>
				<img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/tomato.png">
				<p>${dataArray[i].audience_rating}</p>
				</div>
			</div>
			</div>
				`
				movieRecommend.append(nodeCreated)
			}
			
		})	
}


function main(url) {
	fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {
            let dataArray = datalist; //I will get a list of dict
            console.log(dataArray[0])
			renderMovies(dataArray[0], movieNode);
			let featureStr = dataArray[0].feature_list
			featureList = featureStr.split(',')
			console.log(featureList)
			let featureIdList = []

			featureList.forEach(element => featureIdList.push(featureObject[element]));
			console.log(featureIdList)
			jsonFeatureIdList = JSON.stringify(featureIdList)
			ratingFun()
			heartButton()
			renderRecommend(`/api/movie/recommend?feature=${jsonFeatureIdList}&id=${internalId}`,movieRecommend)
            // let nodeRecommend = document.createElement("div");
            // nodeRecommend.classList.add("movie__recommend");
			// nodeRecommend.innerHTML = `
			// <a class="movie" href="movie/tt8096832">
			// <img src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg" />
			// <div class="movie__info">
			// <h3>綠色奇蹟</h3>
			// <div class="rank">
			// 	<div>
			// 	<img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/imdb.png"/>
			// 	<p>6.3</p>
			// 	</div>
			// 	<div>
			// 	<img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/douban.jpg"/>
			// 	<p>6.90</p>
			// 	</div>
			// 	<div>
			// 	<img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/tomato.png"/>
			// 	<p>80</p>
			// 	</div>
			// </div>
			// </div>
			// </a>
			// `
			// // movieSection.appendChild(nodeRecommend)
        });
}
main(`/api/detail/${internalId}`)






