<template>
	<div>
		<login v-if="!is_auth"/>
		<admin-panel v-else/>

		<div v-if="is_auth" class="container">
			<div class="mb-3">
				<b-button @change="notify()" class="mr-2" @click="sort_by_name()">Сортировать по имени</b-button>
				<b-button @change="notify()" @click="sort_by_price()">Сортировать по цене</b-button>
			</div>
			<b-input @change="reset_page()" class="mb-3" v-model="search"> placeholder="Поиск"></b-input>

			<div>Количество комнат</div>
			<label for="c1">
				<input @change="reset_page()" v-model="c1" id="c1" type="checkbox" name="choice"> 1
			</label>
			<br>
			<label for="c2">
				<input @change="reset_page()" v-model="c2" id="c2" type="checkbox" name="choice"> 2
			</label>
			<br>
			<label for="c3">
				<input @change="reset_page()" v-model="c3" id="c3" type="checkbox" name="choice"> 3
			</label>
			<br>
			<div>
				<label for="price_start">
					цена начало
					<input @change="reset_page()" id="price_start" v-model="start_price" type="number">
				</label>
				<label for="price_end">
					цена конец
					<input @change="reset_page()" id="price_end" v-model="end_price" type="number">
				</label>
			</div>

			<b-table :items="items.results"></b-table>
			<b-button @click="prev()">prev</b-button>
			<b-button @click="next()">next</b-button>
			<div>{{ page }}/{{ items.count }}</div>
		</div>
	</div>
</template>

<script>
import Login from '../components/Login.vue'
import AdminPanel from '../components/Admin-panel'
import axios from 'axios'

export default {
	components: { Login, AdminPanel },
	name: 'Home',
	data () {
		return {
			is_auth: false,
			items: [],
			sort_name: true,
			sort_price: false,
			c1: false,
			c2: false,
			c3: false,
			search: '',
			request: '',
			page: 1,
			next_disable: false,
			prev_disable: true,
			start_price: 0,
			end_price: 0
		}
	},
	mounted () {
		this.is_auth = Boolean(sessionStorage.getItem('auth_token') !== null)
		console.log('http://127.0.0.1:8000/rooms/?search=' + this.search + (this.sort_price ? '&ordering=cost_of_living' : '&ordering=name' + this.c1 ? '&room_type=1' : '' + this.c2 ? '&room_type=2' : '' + this.c3 ? '&room_type=3' : ''))
		this.request = 'http://127.0.0.1:8000/rooms/?search=' + this.search + (this.sort_price ? '&ordering=cost_of_living' : '&ordering=name' + (this.c1 ? '&room_type=1' : '') + (this.c2 ? '&room_type=2' : '') + (this.c3 ? '&room_type=3' : ''))
		axios({
			method: 'get',
			url: this.request,
			responseType: 'json',
			headers: { Authorization: 'Token ' + sessionStorage.getItem('auth_token') }
		}).then((response) => {
			this.items = response.data
			console.log(this.items)
		})
	},
	methods: {
		sort_by_name: function () {
			this.sort_name = true
			this.sort_price = false
			this.notify()
		},
		sort_by_price: function () {
			this.sort_name = false
			this.sort_price = true
			this.notify()
		},
		notify: function () {
			let range = ''
			console.log(this.start_price)
			console.log(this.end_price)
			if (parseInt(this.end_price) > 0 && parseInt(this.start_price) >= parseInt(this.end_price)) {
				this.start_price = this.end_price - 1
			}
			if (parseInt(this.start_price) < parseInt(this.end_price)) {
				range = '&cost_of_living_min=' + this.start_price + '&cost_of_living_max=' + this.end_price
			}
			console.log(this.page)
			axios({
				method: 'get',
				url: 'http://127.0.0.1:8000/rooms/?search=' + this.search + (this.sort_price ? '&ordering=cost_of_living' : '&ordering=name' + (this.c1 ? '&room_type=1' : '') + (this.c2 ? '&room_type=2' : '') + (this.c3 ? '&room_type=3' : '') + range + '&page=' + this.page),
				responseType: 'json',
				headers: { Authorization: 'Token ' + sessionStorage.getItem('auth_token') }
			}).then((response) => {
				this.items = response.data
				console.log(this.items)
			})
		},
		next: function () {
			this.prev_disable = false
			// console.log(this.items.count)

			if (this.items.count > this.page) {
				this.page = this.page + 1
			}
			if (this.items.count === this.page) {
				this.next_disable = true
			}
			console.log(this.page)
			this.notify()
		},
		prev: function () {
			this.next_disable = false

			if (this.page > 1) {
				this.page--
			}
			if (this.page === 1) {
				this.prev_disable = true
			}
			this.notify()
		},
		reset_page: function () {
			this.page = 1
			this.notify()
		}
	}
	// computed: {
	// 	// a computed getter
	// 	request () {
	// 		// `this` points to the component instance
	// 		return 'http://127.0.0.1:8000/rooms/?search=' + this.search + (this.sort_price ? '&ordering=cost_of_living' : '&ordering=name' + (this.c1 ? '&room_type=1' : '') + (this.c2 ? '&room_type=2' : '') + (this.c3 ? '&room_type=3' : ''))
	// 	}
	// }
	// asyncComputed: {
	// 	async items () {
	// 		console.log('sdf')
	// 		return await axios.get(this.request, { headers: { Authorization: 'Token ' + sessionStorage.getItem('auth_token') } })
	// 	}
	// }
}
</script>

<style>

</style>
