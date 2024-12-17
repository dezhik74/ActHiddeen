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
        emptyAct(){
            return {
                id: 0,
                act_number: "",
                act_suffix: "",
                act_date: "",
                begin_date: "",
                end_date: "",
                permitted_work: "",
                presented_work: "",
                work_SNIP: "",
                materials: "",
                docs: "",
                annex: "",
                certificates: [],
            }
        },
        renumerateActs() {
            for (let i = 0; i < this.acts.length; i++) {
                this.acts[i].act_number = String(i+1).padStart(2, '0');
            }
            let counter = this.acts.length
            if (this.my_object.is_washing_purging_act) {
                counter = counter + 1
                this.my_object.w_p_act_number = String(counter).padStart(2, '0');
            }
            if (this.my_object.is_washing_disinfection_act) {
                counter = counter + 1
                this.my_object.w_d_act_number = String(counter).padStart(2, '0');
            }
            if (this.my_object.is_hydraulic_testing_act) {
                counter = counter + 1
                this.my_object.h_act_number = String(counter).padStart(2, '0');
            }
            if (this.my_object.is_sewer_testing_act) {
                counter = counter + 1
                this.my_object.s_t_act_number = String(counter).padStart(2, '0');
            }
            if (this.my_object.is_adjusting_heating_act) {
                counter = counter + 1
                this.my_object.a_act_number = String(counter).padStart(2, '0');
            }
        },
        insertActUp(index) {
            this.acts.splice(index, 0, this.emptyAct());
            this.renumerateActs()
        },
        insertActDown(index) {
            this.acts.splice(index+1, 0, this.emptyAct());
            this.renumerateActs()
        },
        deleteAct(index) {
            this.acts.splice(index, 1);
            this.renumerateActs()
        }

    }
}