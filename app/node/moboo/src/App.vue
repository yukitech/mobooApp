<script setup lang="ts">
import axios from 'axios'
import { reactive } from 'vue'
import imgWalk from './assets/walk.png'
import imgFall from './assets/fall.png'
import imgStand from './assets/standup.png'
import imgSit from './assets/sitdown.png'

type TypePredResult = {
  id: number,
  pred_result: string,
  pred_result_simp: string,
  message: string,
  img: string
}

type TypeProbResult = {
  id: number,
  prob_result: {}
}

type TypeResultAll = {
  id: number,
  file_name: string,
  pred_result: string,
  prob_result?: TypeProbResult,
  pred_result_simp: string,
  prob_result_simp?: TypeProbResult,
  created_at: string
}

const pred_result = reactive<TypePredResult>({
  id: 0,
  pred_result: "",
  pred_result_simp: "",
  message: "",
  img: ""
})

const endPoint: string = 'http://133.130.109.157:8000/get_pred_result'
axios.get(
  endPoint,
).then(
  (response) => {
    pred_result.id = response.data.id

    let img = document.getElementById('pred-img')
    switch(response.data.pred_result) {
      case 'fall':
        pred_result.pred_result = "転倒"
        pred_result.message = "介護者が転倒した可能性があります"
        img?.setAttribute('src', imgFall)
        break
      case "walk":
        pred_result.pred_result = "歩く"
        pred_result.message = "介護者が歩いています"
        pred_result.img = "logo"
        img?.setAttribute('src', imgWalk)
        break
      case "standup":
        pred_result.pred_result = "立つ"
        pred_result.message = "介護者が立ちました"
        img?.setAttribute('src', imgStand)
        break
      case "sitdown":
        pred_result.pred_result = "座る"
        pred_result.message = "介護者が座りました"
        img?.setAttribute('src', imgSit)
        break
    }

    switch(response.data.pred_result_simp) {
      case "move":
        pred_result.pred_result_simp = "動く"
        break
      case "static":
        pred_result.pred_result_simp = "静止"
        break
    }
    console.log(pred_result)
  }
).catch(
  () => {
    alert("エラーが発生しました！")
  }
)

const prob_result = reactive<TypeProbResult>({
  id: 0,
  prob_result: {}
})

const get_prob_result = (id: number)  => {
  const endPoint: string = `http://133.130.109.157:8000/get_prob_result/${id}`
  axios.get(
    endPoint
  ).then(
    (response) => {
      const json_pred = JSON.parse(response.data.pred_result.replace(/'/g, '\"'))
      let new_pred: {[key: string]: number}
      new_pred = {}
      for (let key in json_pred) {
        let new_value = parseFloat(json_pred[key])*100
        switch(key) {
          case 'fall':
            new_pred["転倒"] = new_value
            break
          case "walk":
            new_pred["歩く"] = new_value
            break
          case "standup":
            new_pred["立つ"] = new_value
            break
          case "sitdown":
            new_pred["座る"] = new_value
            break
        }
      }
      prob_result.id = response.data.id
      prob_result.prob_result = new_pred
    }
  ).catch(
    (e) => {
      console.log(e)
      alert("エラーが発生しました！")
  }
  )
}

let result_all: TypeResultAll[] = []

const get_all_url: string = 'http://133.130.109.157:8000/all'
axios.get(
  get_all_url,
).then(
  (response) => {
    covert_action_name(response.data)
    result_all= response.data
  }
).catch(
  () => {
    alert("エラーが発生しました！")
  }
)

const covert_action_name = (old_data: TypeResultAll[])  => {
  for(let i in old_data) {
    switch(old_data[i].pred_result) {
      case 'fall':
        old_data[i].pred_result = "転倒"
        break
      case "walk":
        old_data[i].pred_result = "歩く"
        break
      case "standup":
        old_data[i].pred_result = "立つ"
        break
      case "sitdown":
        old_data[i].pred_result = "座る"
        break
    }
    switch(old_data[i].pred_result_simp) {
      case 'move':
        old_data[i].pred_result_simp = "動く"
        break
      case "static":
        old_data[i].pred_result_simp = "静止"
        break
    }
  }
}

</script>

<template>
  <header class="bg-blue-100">
    <div class="navbar w-4/5 mx-auto">
      <div class="flex-1">
        <a href="#" class="logo">
          <img class="w-60" src="./assets/logo.png" alt="ロゴ画像です">
        </a>
      </div>
      <div class="flex-none">
        <ul class="menu menu-horizontal bg-bule-100 rounded-box mt-6">
          <li>
            <a class="tooltip" data-tip="ホーム">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-11/12 sm:h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
            </a>
          </li>
          <li>
            <a class="tooltip" data-tip="行動履歴">
              <svg xmlns="http://www.w3.org/2000/svg" class="sm:h-7 w-7 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            </a>
          </li>
          <li>
            <a class="tooltip" data-tip="アプリ説明">
              <svg xmlns="http://www.w3.org/2000/svg" class="sm:h-7 w-7 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </header>
  <main class="bg-gray-100 py-10">
    <div class="divider divider-neutral w-1/2 mx-auto text-3xl mb-10">現在の行動</div>
    <div class="card w-1/2 bg-base-100 shadow-xl mx-auto" :class="{'bg-red-100':  pred_result.pred_result == '転倒' }">
      <figure class="px-10 pt-10">
        <img src="" alt="推定行動の画像" max-h-64 class="rounded-xl" id="pred-img"/>
      </figure>
      <div class="card-body items-center text-center">
        <h2 class="card-title">
          {{ pred_result.pred_result }}
          <span class="badge badge-primary badge-outline">
            {{ pred_result.pred_result_simp }}
          </span>
        </h2>
        <p>{{ pred_result.message }}</p>
        <div class="card-actions">
          <button class="btn btn-primary" onclick="my_modal_2.showModal()" v-on:click="get_prob_result(pred_result.id)">予測結果の表示</button>
        </div>
      </div>
    </div>

    <dialog id="my_modal_2" class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-center">推定結果</h3>
        <ul class="text-center" v-for="(value, key) in prob_result.prob_result">
          <li>{{ key }} : {{ value }}%</li>
        </ul>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>

    <div class="divider divider-neutral w-1/2 mx-auto text-3xl mt-20 mb-10">行動履歴</div>

    <div class="card w-4/5 bg-base-100 m-20 shadow-xl mx-auto">
      <div class="card-body items-center text-center">
        <div class="overflow-x-auto overflow-y-auto h-96 w-11/12">
          <table class="table mx-auto">
            <!-- head -->
            <thead>
              <tr>
                <th></th>
                <th>タイムスタンプ</th>
                <th>推定行動</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="result in result_all" :class="{'bg-red-100':  result.pred_result == '転倒' }">
                <th >{{ result.id }}</th>
                <td>{{ result.created_at }}</td>
                <td>
                  {{ result.pred_result }}
                  <span class="badge badge-primary badge-outline">
                    {{ result.pred_result_simp }}
                  </span>
                </td>
                <td>
                  <div class="card-actions">
                    <button class="btn btn-primary btn-sm" onclick="my_modal_2.showModal()" v-on:click="get_prob_result(result.id)">予測結果の表示</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </main>
</template>