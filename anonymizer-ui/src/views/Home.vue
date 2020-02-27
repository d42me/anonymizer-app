<template>
  <div class="home">
    <div class="main-container">
      <div class="inner-wrapper">
        <h1>
          Welcome to
          <b>🕵️‍♀️ Anonymizer</b>
        </h1>
        <h4>We anonymize your docs. Just upload a PDF file.</h4>
        <b-form class="form" v-if="!loading && !result" @submit="onSubmit">
          <b-form-file
            v-model="file"
            placeholder="Upload document"
            accept="pdf/*"
            class="file-input"
            required
          ></b-form-file>
          <b-button type="submit" class="submit-btn" variant="outline-primary">Submit</b-button>
        </b-form>
        <h6 v-if="loading && !result">Just a moment we are uploading and processing your document...</h6>
        <b-jumbotron class="center" :lead="result" v-if="result">
          <b-button @click="resetForm" variant="outline-primary">Try again</b-button>
        </b-jumbotron>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "home",
  components: {},
  data() {
    return {
      file: null,
      loading: false,
      result: null,
      bgImage: null
    };
  },
  methods: {
    async onSubmit(evt) {
      evt.preventDefault();
      this.loading = true;
      let formData = new FormData();
      formData.append("file", this.file);
      var self = this;
      let res = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        timeout: 180000
      });
      console.log("result");
      self.loading = false;
      self.result = "Here is your anonymized result text:\n\n\n" + res.data;
    },
    resetForm() {
      this.file = null;
      this.loading = false;
      this.result = null;
      this.bgImage = null;
    }
  }
};
</script>
<style lang="scss">
.home {
  margin: 0;
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: row;
}

.main-container {
  position: relative;
  display: flex;
  width: 100%;

  .inner-wrapper {
    padding: 5%;
    text-align: left;
    h1 {
      color: #111;
    }

    h4 {
      margin-bottom: 2rem;
    }
  }

  .text-left {
    text-align: left;
  }
}

.form {
  .file-input {
    width: 70%;
  }

  .submit-btn {
    width: 20%;
    margin-left: 5%;
  }
}

@media only screen and (max-width: 480px) {
  .home {
    flex-direction: column;
  }

  .main-container {
    width: 100%;
    height: auto;

    .inner-wrapper {
      padding: 10% 9%;
    }
  }

  .form {
    .file-input {
      width: 100%;
    }

    .submit-btn {
      width: 40%;
      margin-left: 0;
      margin-top: 10%;
    }
  }
}
</style>
