const databaseStatusTable = document.querySelector(".table__value")
const ImdbStatusTable = document.querySelector(".IMDb_table_data")
const startDate = document.querySelector('input[name="startDate"]')
const endDate = document.querySelector('input[name="endDate"]')

let today_date = new Date().toLocaleDateString().replace("/","-").replace("/","-");
if (today_date.slice(5,6) != 0){
    today_date = today_date.slice(0,5)+ "0"+ today_date.slice(5)
}

endDate.value = today_date
function formatDate(date){
    return date.slice(-5).replace("-","/")
}

function renderMovieUpdatePlot(object,title,nodeId){
    let datesArray = []
    let successDataArray = []
    let failedDataArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        successDataArray.push(i.new_douban_amount-i.douban_failed_amount)
        failedDataArray.push(i.douban_failed_amount)
    }
    let trace1 = {
        x: datesArray,
        y: successDataArray,
        type: 'bar',
        name : '更新成功數'
    };
    
    let trace2 = {
        x: datesArray,
        y: failedDataArray,
        type: 'bar',
        name : '更新失敗數'
    }
    
    let  layout = {
        barmode: 'stack',
        title: {
        text:title,
        },
        legend: {
            "orientation": "h",
            "y" : 1.16
        },
    }
    let data = [trace1, trace2];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderTomatoUpdatePlot(object,title,nodeId){
    let datesArray = []
    let successDataArray = []
    let failedDataArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        successDataArray.push(i.new_tomato_amount-i.tomato_failed_amount)
        failedDataArray.push(i.tomato_failed_amount)
    }
    let trace1 = {
        x: datesArray,
        y: successDataArray,
        type: 'bar',
        name : '更新成功數'
    };
    
    let trace2 = {
        x: datesArray,
        y: failedDataArray,
        type: 'bar',
        name : '更新失敗數'
    }
    
    let  layout = {
        barmode: 'stack',
        title: {
        text:title,
        },
        legend: {
            "orientation": "h",
            "y" : 1.16,
            
        },
    }
    let data = [trace1, trace2];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderFetchDetailTimePlot(object,title,nodeId){
    let datesArray = []
    let doubanDataArray = []
    let tomatoDataArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        doubanDataArray.push(i.douban_fetch_avg_time)
        tomatoDataArray.push(i.tomato_fetch_avg_time)
    }
    let trace1 = {
        x: datesArray,
        y: doubanDataArray,
        type: 'scatter',
        name : '豆瓣爬取時間(秒）'
    };
    
    let trace2 = {
        x: datesArray,
        y: tomatoDataArray,
        type: 'scatter',
        name : '爛番茄爬取時間(秒）'
    }
    
    let  layout = {
        title: {
        text:title,
        },
        legend: {
            "orientation": "h",
            "y" : 1.16,
            'bordercolor': 'rgb(255,0,0)'
        },
    }
    let data = [trace1, trace2];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderDatabaseStatusTable(object){
    let htmlText = ''
    let addText 
    for (let i of object) {
        console.log(i)
        addText = `<tr>
        <td>${formatDate(i.update_date)}</td>
        <td>${i.insert_mysql_status}</td>
        <td>${i.insert_amount}</td>
        </tr>`
        htmlText = addText + htmlText
    }
    databaseStatusTable.innerHTML = htmlText
}
function renderDoubanRotateRatePlot(object,title,nodeId){
    let datesArray = []
    let doubanDataArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        doubanDataArray.push(i.new_douban_amount/i.new_imdb_amount)
    }
    let trace1 = {
        x: datesArray,
        y: doubanDataArray,
        type: 'scatter',
        name : 'IMDB-豆瓣轉換率',
    };
    let  layout = {
        title: {
        text:title,
        },
        yaxis: {
            range: [0, 1]
          },
        legend: {
            "orientation": "h",
            "y" : 1.16
        },
    }
    let data = [trace1];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderTomatoRotateRatePlot(object,title,nodeId){
    let datesArray = []
    let tomatoDataArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        tomatoDataArray.push(i.new_tomato_amount/i.new_douban_amount)
    }
    let trace1 = {
        x: datesArray,
        y: tomatoDataArray,
        type: 'scatter',
        name : '豆瓣-爛番茄轉換率',
    };
    let  layout = {
        title: {
        text:title,
        },
        legend: {
            "orientation": "h",
            "y" : 1.16
        },
        yaxis: {
            range: [0, 1]
          },
    }
    let data = [trace1];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderImdbStatusTable(object){
    let htmlText = ''
    let addText 
    for (let i of object) {
        console.log(i)
        addText = `<tr>
        <td>${formatDate(i.update_date)}</td>
        <td>${i.new_imdb_amount}</td>
        <td>${i.imdb_fetch_time}</td>
        <td>${i.google_fetch_avg_time}</td>
        </tr>`
        htmlText = addText + htmlText
    }
    ImdbStatusTable.innerHTML = htmlText
}
function renderMovieDetailRelateDataPlot(url) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((dataObject) => {
            renderMovieUpdatePlot(dataObject,"電影新增狀況",'myDiv1')
            renderTomatoUpdatePlot(dataObject,"爛番茄新增狀況",'myDiv')
            renderFetchDetailTimePlot(dataObject,"爬取時間","myDiv2")
            renderDatabaseStatusTable(dataObject)
            renderDoubanRotateRatePlot(dataObject,"IMDb - 豆瓣轉換率","myDiv7")
            renderTomatoRotateRatePlot(dataObject,"豆瓣 - 爛番茄轉換率","myDiv8")
            renderImdbStatusTable(dataObject)
        })
        .catch((error) => {
            console.log('Error:', error)
        })

}


let moviePipelineFetchUrl = `/api/movie_status/?start=${startDate.value}&end=${endDate.value}`
renderMovieDetailRelateDataPlot(moviePipelineFetchUrl)

function renderImdbRatingPlot(object,title,nodeId){
    let datesArray = []
    let getRatingArray = []
    let nonRatingArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        getRatingArray.push(i.update_imdb_amount-i.not_rating_imdb_amount)
        nonRatingArray.push(i.not_rating_imdb_amount)
    }
    let trace1 = {
        x: datesArray,
        y: getRatingArray,
        type: 'bar',
        name : '成功更新數'
    };
    
    let trace2 = {
        x: datesArray,
        y: nonRatingArray,
        type: 'bar',
        name : '尚未有評分'
    }
    
    let  layout = {
        barmode: 'stack',
        title: {
        text:title,
        },
        legend: {
            "orientation": "h",
            "y" : 1.16
        },
    }
    let data = [trace1, trace2];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderDoubanRatingPlot(object,title,nodeId){
    let datesArray = []
    let getRatingArray = []
    let nonRatingArray = []
    let failedUpdateArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        getRatingArray.push(i.update_douban_amount-i.not_rating_douban_amount-i.fail_douban_amount)
        nonRatingArray.push(i.not_rating_douban_amount)
        failedUpdateArray.push(i.fail_douban_amount)
    }
    let trace1 = {
        x: datesArray,
        y: getRatingArray,
        type: 'bar',
        name : '成功更新數'
    };
    
    let trace2 = {
        x: datesArray,
        y: nonRatingArray,
        type: 'bar',
        name : '尚未有評分'
    }
    let trace3 = {
        x: datesArray,
        y: failedUpdateArray,
        type: 'bar',
        name : '更新失敗',
        text: failedUpdateArray.map(String),
        marker: {
            color: 'rgb(255,0,0)',
            opacity: 0.6,
          }

    }
    let  layout = {
        barmode: 'stack',
        title: {
        text:title,
        },
        legend: {
            "orientation": "h",
            "y" : 1.16
        },
    }
    let data = [trace1, trace2,trace3];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderTomatoRatingPlot(object,title,nodeId){
    let datesArray = []
    let getRatingArray = []
    let nonRatingArray = []
    let failedUpdateArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        getRatingArray.push(i.update_tomato_amount-i.not_rating_tomato_amount-i.fail_tomato_amount)
        nonRatingArray.push(i.not_rating_tomato_amount)
        failedUpdateArray.push(i.fail_tomato_amount)
    }
    let trace1 = {
        x: datesArray,
        y: getRatingArray,
        type: 'bar',
        name : '成功更新數'
    };
    
    let trace2 = {
        x: datesArray,
        y: nonRatingArray,
        type: 'bar',
        name : '尚未有評分'
    }
    let trace3 = {
        x: datesArray,
        y: failedUpdateArray,
        type: 'bar',
        name : '更新失敗',
        text: failedUpdateArray.map(String),
        marker: {
            color: 'rgb(255,0,0)',
            opacity: 0.6,
          }

    }
    let  layout = {
        barmode: 'stack',
        title: {
        text:title,
        },
        legend: {
            "orientation": "h",
            "y" : 1.16
        },
    }
    let data = [trace1, trace2,trace3];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderFetchRatingTimePlot(object,title,nodeId){
    let datesArray = []
    let doubanDataArray = []
    let tomatoDataArray = []
    for (let i of object) {
        datesArray.push(formatDate(i.update_date))
        doubanDataArray.push(i.avg_douban_fetch_time)
        tomatoDataArray.push(i.avg_tomato_fetch_time)
    }
    let trace1 = {
        x: datesArray,
        y: doubanDataArray,
        type: 'scatter',
        name : '豆瓣爬取時間(秒）'
    };
    
    let trace2 = {
        x: datesArray,
        y: tomatoDataArray,
        type: 'scatter',
        name : '爛番茄爬取時間(秒）'
    }
    
    let  layout = {
        title: {
        text:title,
        },
        legend: {
            "orientation": "h",
            "y" : 1.16
        },
    }
    let data = [trace1, trace2];
    
    Plotly.newPlot(nodeId, data, layout);
}
function renderRatingDetailRelateDataPlot(url) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((dataObject) => {
            console.log(dataObject)
            renderImdbRatingPlot(dataObject,"IMDb 評分更新狀態","myDiv3")
            renderDoubanRatingPlot(dataObject,"豆瓣評分更新狀態","myDiv4")
            renderTomatoRatingPlot(dataObject,"爛番茄評分更新狀態","myDiv5")
            renderFetchRatingTimePlot(dataObject,"評分爬取時間","myDiv6")
        })
        .catch((error) => {
            console.log('Error:', error)
        })

}
let ratingPipelineFetchUrl = `/api/rating_status/?start=${startDate.value}&end=${endDate.value}`
renderRatingDetailRelateDataPlot(ratingPipelineFetchUrl)
startDate.addEventListener("change",() =>{
    moviePipelineFetchUrl = `/api/movie_status/?start=${startDate.value}&end=${endDate.value}`
    renderMovieDetailRelateDataPlot(moviePipelineFetchUrl)
    ratingPipelineFetchUrl = `/api/rating_status/?start=${startDate.value}&end=${endDate.value}`
    renderRatingDetailRelateDataPlot(ratingPipelineFetchUrl)

})
endDate.addEventListener("change",() =>{
    moviePipelineFetchUrl = `/api/movie_status/?start=${startDate.value}&end=${endDate.value}`
    renderMovieDetailRelateDataPlot(moviePipelineFetchUrl)
    ratingPipelineFetchUrl = `/api/rating_status/?start=${startDate.value}&end=${endDate.value}`
    renderRatingDetailRelateDataPlot(ratingPipelineFetchUrl)

})
// renderPlot(renderMovieUpdatePlot,"電影新增狀況",ratingFetchUrl,'myDiv1')
// renderPlot(renderTomatoUpdatePlot,"爛番茄新增狀況",ratingFetchUrl,'myDiv')
// renderPlot(renderFetchDetailTimePlot,"爬取時間",ratingFetchUrl,'myDiv2')




// let trace1 = {
//     x: ['07/12', '07/13', '07/14'],
//     y: [20, 14, 23],
//     name: '更新評分成功',
//     type: 'bar'
// };

// let trace2 = {
//     x: ['07/12', '07/13', '07/14'],
//     y: [12, 18, 29],
//     name: '更新評分失敗',
//     type: 'bar',
    
// };

// let  layout = {
//     barmode: 'stack',
//     title: {
//     text:'Plot Title',
//     },
//     legend: {
//         "orientation": "h",
//         "y" : 1.16
//     },
// }
// let data = [trace1, trace2];

// // Plotly.newPlot('myDiv', data, layout);
// // Plotly.newPlot('myDiv2', data, layout);
// // Plotly.newPlot('myDiv3', data, layout);
// Plotly.newPlot('myDiv4', data, layout);

// Plotly.newPlot('myDiv5', data, layout);
// Plotly.newPlot('myDiv6', data, layout);
// Plotly.newPlot('myDiv7', data, layout);
// Plotly.newPlot('myDiv8', data, layout);