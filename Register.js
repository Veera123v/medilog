
import React, { useContext } from 'react';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { TextField, Button, Typography, Paper } from '@mui/material';
import AuthContext from '../../context/authContext';

const RegisterSchema = Yup.object().shape({
  name: Yup.string().required('Required'),
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(6, 'Too Short!').required('Required'),
});

const Register = () => {
  const auth = useContext(AuthContext);

  return (
    <Paper style={{ padding: '20px', maxWidth: '400px', margin: '40px auto' }}>
      <Typography variant="h5" gutterBottom>
        Register
      </Typography>
      <Formik
        initialValues={{
          name: '',
          email: '',
          password: '',
        }}
        validationSchema={RegisterSchema}
        onSubmit={(values, { setSubmitting }) => {
          auth.register(values);
          setSubmitting(false);
        }}
      >
        {({ errors, touched, isSubmitting }) => (
          <Form>
            <Field
              as={TextField}
              name="name"
              label="Name"
              fullWidth
              margin="normal"
              error={touched.name && !!errors.name}
              helperText={touched.name && errors.name}
            />
            <Field
              as={TextField}
              name="email"
              label="Email"
              fullWidth
              margin="normal"
              error={touched.email && !!errors.email}
              helperText={touched.email && errors.email}
            />
            <Field
              as={TextField}
              name="password"
              label="Password"
              type="password"
              fullWidth
              margin="normal"
              error={touched.password && !!errors.password}
              helperText={touched.password && errors.password}
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={isSubmitting}
              style={{ marginTop: '20px' }}
            >
              Register
            </Button>
          </Form>
        )}
      </Formik>
    </Paper>
  );
};

export default Register;