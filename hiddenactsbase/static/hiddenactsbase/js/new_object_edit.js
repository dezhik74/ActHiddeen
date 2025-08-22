function formManager() {
    return {
        // data from API
        my_object: {},
        acts: [],
        all_certs: [],
        // data for UI
        loading: false,
        error: "",
        success: "",
        // data for certificates modal
        modal: {},
        selectedCerts: [],
        modalAct: {},
        yearCertFilter: "",
        filteredCerts: [],
        // data for "steal acts modal"
        stealActsModal: {},
        allObjects: [],
        selectedObjects: [],
        stealFilter: "",
        objectForStealId: "",

        async init() {
            const objId = document.getElementById("object_id").value;
            this.modal = new bootstrap.Modal(document.getElementById('myModal'))
            this.stealActsModal = new bootstrap.Modal(document.getElementById('stealModal'))
            await this.loadData(objId)
        },
        async loadData(objId) {
            this.loading = true;
            this.error = "";
            try {
                const response = await axios.get(`/api/get-object/${objId}`);
                this.my_object = response.data.my_object
                this.acts = response.data.acts;
                this.all_certs = response.data.all_certs;
            } catch (err) {
                this.error = "Не удалось загрузить данные из API.";
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        async loadAllObjects() {
            this.loading = true;
            this.error = "";
            try {
                const response = await axios.get(`/api/get-all-objects/`);
                this.allObjects = response.data;
            } catch (err) {
                this.error = "Не удалось загрузить данные всех объектов из API.";
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        async sendResults() {
            this.error = "";
            this.success = "";
            this.loading = true;
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
            } finally {
                this.loading = false;
            }
        },
        emptyAct() {
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
                this.acts[i].act_number = String(i + 1).padStart(2, '0');
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
            this.acts.splice(index + 1, 0, this.emptyAct());
            this.renumerateActs()
        },
        deleteAct(index) {
            this.acts.splice(index, 1);
            this.renumerateActs()
        },
        swapActs(index) {
            if (index < this.acts.length - 1) {
                const temp = this.acts[index];
                this.acts[index] = this.acts[index + 1];
                this.acts[index + 1] = temp;
                this.renumerateActs()
            }
        },
        changeActsDate(date, date_type) {
            for (let i = 0; i < this.acts.length; i++) {
                switch (date_type) {
                    case "begin": {
                        this.acts[i].begin_date = date;
                        break;
                    }
                    case "end": {
                        this.acts[i].end_date = date;
                        break;
                    }
                    case "act": {
                        this.acts[i].act_date = date;
                        break;
                    }
                }
            }
            if (date_type == "act") {
                this.my_object.w_p_act_date = date;
                this.my_object.w_d_act_date = date;
                this.my_object.h_act_date = date;
                this.my_object.s_t_act_date = date;
                this.my_object.a_act_date = date;
            }
        },
        showAndInitModal(act) {
            this.selectedCerts = act.certificates.map(cert => cert.id);
            this.modalAct = act;
            this.updateFilteredCerts();
            this.modal.show()
        },
        updateFilteredCerts() {
            this.filteredCerts = this.all_certs.filter(cert => cert.year.toLowerCase().includes(this.yearCertFilter.toLowerCase()));
        },
        saveModal(modalAct) {
            modalAct.certificates = this.selectedCerts.map(id => this.all_certs.find(cert => cert.id == id));
            this.modal.hide();
        },
        async showAndInitStealActsModal() {
            await this.loadAllObjects();
            this.updateSelectedObjects();
            this.stealActsModal.show()
        },
        updateSelectedObjects() {
            this.selectedObjects = this.allObjects.filter(obj => obj.address.toLowerCase().includes(this.stealFilter.toLowerCase()));
        },
        async loadObjectActs(objId){
            this.loading = true;
            this.error = "";
            try {
                const response = await axios.get(`/api/get-object-acts/${objId}`);
                const objectActs = response.data;
                objectActs.forEach((act) => {
                    act.id = 0;
                    this.acts.push(act);
                })
                this.renumerateActs();
            } catch (err) {
                this.error = "Не удалось загрузить данные из API.";
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        async saveStealModal() {
            console.log('asdfasdf', this.objectForStealId);
            await this.loadObjectActs(this.objectForStealId)
            this.stealActsModal.hide();
        },
        setCertificates() {
            console.log(this.acts)
            this.acts.forEach((act) => {
                let materials = "-"
                let annex = "исполнительная схема, "
                let docs = "исполнительная схема."
                if (act.certificates.length > 0) {
                    materials = act.certificates.reduce((acc, cert) => {
                        return acc + `${cert.material_name} (${cert.certificate_requisites}), `
                    }, "").replace(/, $/, '.')
                    annex = act.certificates.reduce((acc, cert) => {
                        return acc + `${cert.certificate_requisites}, `
                    }, "исполнительная схема, ")
                    docs = "исполнительная схема, сертификаты/свидетельства."
                }
                act.materials = materials
                act.annex = annex.replace(/, $/, '.').replace(/\.+$/, '.')
                act.docs = docs
            })
        }
    }
}