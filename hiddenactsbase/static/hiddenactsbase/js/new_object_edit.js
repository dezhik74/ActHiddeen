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
    }
}