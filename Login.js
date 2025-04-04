import React, { useContext } from 'react';
import { Formik, Form, Field } from 'formik';
import {object, string} from 'yup';
import { TextField, Button, Typography, Paper } from '@mui/material';
import AuthContext from '../../context/authContext';

const LoginSchema = object().shape({
  email: string().email('Invalid email').required('Required'),
  password: string().required('Required'),
});

const Login = () => {
  const auth = useContext(AuthContext);

  return (
    <Paper style={{ padding: '20px', maxWidth: '400px', margin: '40px auto' }}>
      <Typography variant="h5" gutterBottom>
        Login
      </Typography>
      <Formik
        initialValues={{
          email: '',
          password: '',
        }}
        validationSchema={LoginSchema}
        onSubmit={(values, { setSubmitting }) => {
          auth.login(values);
          setSubmitting(false);
        }}
      >
        {({ errors, touched, isSubmitting }) => (
          <Form>
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
              Login
            </Button>
          </Form>
        )}
      </Formik>
    </Paper>
  );
};

export default Login;