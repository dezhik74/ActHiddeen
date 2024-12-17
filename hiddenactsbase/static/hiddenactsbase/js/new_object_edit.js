function formManager() {
    return {
        my_object: {},
        acts: [],
        all_certs: [],
        loading: false,
        error: "",
        success: "",

        init() {
            const objId = document.getElementById("object_id").value;
            this.loadData(objId)
        },
        async loadData(objId) {
            this.loading = true;
            this.error = "";
            try {
                const response = await axios.get(`/api/get-object/${objId}`);
                this.my_object = response.data.my_object
                this.acts = response.data.acts;
                this.all_certs = response.data.all_certs;
                console.log(this.my_object);
                console.log(this.acts);
                console.log(this.all_certs);
            } catch (err) {
                this.error = "Не удалось загрузить данные из API.";
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        async sendResults() {
            this.error = "";
            this.success = "";
            const tokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
            axios.defaults.headers.common['X-CSRFToken'] = tokenInput ? tokenInput.value : '';
            try {
                const response = await axios.post(`/api/results/`, {
                    result: {
                        my_object: this.my_object,
                        acts: this.acts,
                    }
                });
                this.success = "Список успешно отправлен!";
                setTimeout(() => {
                    this.success = "";
                }, 1000);
            } catch (err) {
                this.error = "Не удалось отправить данные на API.";
                console.error(err);
            }
        },

    }
}